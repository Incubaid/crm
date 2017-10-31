import os
import subprocess

import ujson as json
from redis import from_url as redis_from_url

from crm.db import RootModel, BaseModel
from crm import app


def _add_to_git(data_dir, file_paths, username):
    """
    Given Data_DIR / Repo, some absolute paths in that Repo and a username
    Add these files to repo and commit changes
    
    :param data_dir: DATA_DIR repo -- place where dumped DB json files live
    :param file_paths: newly created / updated or deleted files
    :param username: username to use as --author during a commit
    :return: 
    """
    dot_git = os.path.abspath(os.path.join(data_dir, '.git'))

    p = subprocess.Popen(
        [
            'git',
            '--git-dir=%s' % dot_git,
            '--work-tree=%s' % os.path.abspath(data_dir),
            'add',
            ' '.join(file_paths)
        ]
    )

    out1, out2 = p.communicate()

    if not p.returncode == 0:
        print('Error adding files to git')
        print( out1, out2)
        exit(1)

    p = subprocess.Popen(
        [
            'git',
            '--git-dir=%s' % dot_git,
            '--work-tree=%s' % os.path.abspath(data_dir),
            'commit',
            '-m',
            'Updated DB',
            '--author',
            '%s <%s@incubaid.com>' % (username, username)
        ]
    )

    out1, out2 = p.communicate()

    if not p.returncode == 0:
        print('Error committing files to git')
        print( out1, out2)
        exit(1)


def _get_cache_client():
    """
    # we use bare python redis client to get list of all keys
    # since this is not supported in the flask cache
    :return: redis connection 
    """

    config = app.cache.config
    cache_type = config['CACHE_TYPE']
    if cache_type != 'redis':
        print('NOT SUPPORTED CACHE BACKEND, ONLY SUPPORTED IS (redis)')
        exit(1)
    try:
        return redis_from_url(app.cache.config['CACHE_REDIS_URL'])
    except:
        print('BAD REDIS URL PROVIDED BY (CACHE_BACKEND_URI)')
        exit(1)


def _ensure_dirs(path):
    """
    Ensure a directory and sub directory exist if not there
    :param dir: 
    :return: 
    """
    if not os.path.exists(path):
        os.makedirs(path)


def _is_root_model(model_name):
    """
    determine whether a model name i.e 'Contact' is a root model or not
    :param name: model name
    :return: True/False
    :rtype: bool
    """
    for klass in RootModel.__subclasses__():
        if klass.__name__ == model_name:
            return True
    return False


def _create_json_file(data_dir, data, model_str):
    if len(model_str) > 100:
        model_str = model_str[:100]

    model_dir = os.path.abspath(os.path.join(data_dir, data['model']))
    _ensure_dirs(model_dir)

    record_path = os.path.abspath(os.path.join(
        model_dir, '%s_%s.json' % (data['id'], model_str)))
    with open(record_path, 'w') as f:
        json.dump(data, f, indent=4, sort_keys=True)
    return record_path


def _delete_json_file(data_dir, data, model_str):

    if len(model_str) > 100:
        model_str = model_str[:100]

        model_dir = os.path.abspath(os.path.join(data_dir, data['model']))

    record_path = os.path.abspath(os.path.join(
        model_dir, '%s_%s.json' % (data['id'], model_str)))
    try:
        os.remove(record_path)
    except:
        print('Error deleting file %s' % record_path)

    return record_path


def _update_fs(items, data_dir, delete=False):
    """
    CREATE OPERATION HANDLING IS CONCERNED ONLY ABOUT ROOT models
    NON ROOT MODEL ITEMS ARE IGNORED

    We don't dump non-root models, since they belong to one root model
    any way and there data will be saved as part of a root model.
    example, if user created a task (non root model) and assigned it to contact
    cached data will look like
    {'changes': {'updated': IdentitySet([<crm.contact.models.Contact object at 0x7f5748a1f5c0>]),
    'deleted': IdentitySet([]),
    'created': IdentitySet([<crm.task.models.Task object at 0x7f574929dba8>])}}
    so Contact object has been updated any way and we'll handle that update add the task in contact data
    in File system.

    :param items: list of model dictionaries that was created
    :param data_dir: where to save files
    :return: newly created file paths
    :rtype: list
    """

    paths = []
    for item in items:
        data = item['data']
        if not _is_root_model(data['model']):
            continue
        if not delete:
            path = _create_json_file(data_dir, data, item['obj_as_str'])
        else:
            path = _delete_json_file(data_dir, data, item['obj_as_str'])
        paths.append(path)
    return paths


@app.cli.command()
def dumpcache():
    """
    Dump root objects in Cache
    We support only redis from now
    """

    data_dir = app.config["DATA_DIR"]
    _ensure_dirs(data_dir)
    cache_client = _get_cache_client()

    current_kyes = cache_client.keys()[:]
    current_kyes.sort()

    for key in current_kyes:
        key = key.replace(b'flask_cache_', b'').decode()
        cached = app.cache.get(key)

        created = cached['created']
        updated = cached['updated']
        deleted = cached['deleted']
        username = cached['username']

        file_paths = []

        file_paths.extend(_update_fs(created, data_dir))
        file_paths.extend(_update_fs(updated, data_dir))
        file_paths.extend(_update_fs(deleted, data_dir, delete=True))
        _add_to_git(data_dir, set([path for path in file_paths if path]), username)

        app.cache.delete(key)
