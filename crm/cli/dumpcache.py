import os
import subprocess

import ujson as json
from redis import from_url as redis_from_url

from crm.db import RootModel
from crm import app


def _add_to_git(files):
    pass


def _commit():
    pass


def _get_cache_client():
    """
    # we use bare python redis client to get list of all keys
    # since this is not supported in the flask cache
    :return: redis
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


def _ensure_dir(data_dir):
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)


def _get_root_model_from_name(name):
    for klass in RootModel.__subclasses__():
        if klass.__name__ == name:
            return klass


def _handle_created_record(item, data_dir):
    """
    CREATE OPERATION HANDLING IS CONCERNED ONLY ABOUT ROOT models

    We don't dump non-root models, since they belong to one root model
    any way and there data will be saved as part of a root model.
    example, if user created a task (non root model) and assigned it to contact
    cached data will look like
    {'changes': {'updated': IdentitySet([<crm.contact.models.Contact object at 0x7f5748a1f5c0>]),
    'deleted': IdentitySet([]),
    'created': IdentitySet([<crm.task.models.Task object at 0x7f574929dba8>])}}
    so Contact object has been updated any way and we'll handle that update add the task in contact data
    in File system.

    :param item: model dictionary that was created
    :param data_dir: where to save files
    """

    data = item['data']

    root_model = DumpCacheUtils._get_root_model_from_name(data['model'])

    if not root_model:
        return

    obj_as_str = item['obj_as_str']

    if len(obj_as_str) > 100:
        obj_as_str = obj_as_str[:100]

    model_dir = os.path.abspath(os.path.join(data_dir, data['model']))
    DumpCacheUtils._ensure_dir(model_dir)

    record_path = os.path.abspath(os.path.join(
        model_dir, '%s_%s.json' % (data['id'], obj_as_str)))
    with open(record_path, 'w') as f:
        json.dump(data, f, indent=4, sort_keys=True)

    dot_git = os.path.abspath(os.path.join(data_dir, '.git'))
    subprocess.call(
        [
            'git',
            '--git-dir=%s' % dot_git,
            '--work-tree=%s' % os.path.abspath(data_dir),
            'add',
            record_path
        ]
    )


def _handle_updated_record(item, data_dir):
    pass


def _handle_deleted_record(item, data_dir):
    pass


@app.cli.command()
def dumpcache():
    """
    Dump root objects in Cache
    We support only redis from now
    """

    data_dir = app.config["DATA_DIR"]
    _ensure_dir(data_dir)
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

        for item in created:
            _handle_created_record(item, data_dir)

        for item in updated:
            _handle_updated_record(item, data_dir)

        for item in deleted:
            _handle_deleted_record(item, data_dir)

        dot_git = os.path.abspath(os.path.join(data_dir, '.git'))

        subprocess.call(
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

        app.cache.delete(key)
