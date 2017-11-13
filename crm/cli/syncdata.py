import time
import os
import subprocess

from crm import app
from crm.cli.dumpcache import _dump


def _push(number_commits):
    print('\n\t\t\033[94mPUSHING %d COMMITS(s) TO REMOTE REPO\033[0m\n' % number_commits)
    data_dir = app.config["DATA_DIR"]
    dot_git = os.path.abspath(os.path.join(data_dir, '.git'))

    p = subprocess.Popen(
        [
            'git',
            '--git-dir=%s' % dot_git,
            '--work-tree=%s' % os.path.abspath(data_dir),
            'push'
        ]
    )

    out1, out2 = p.communicate()

    if not p.returncode == 0:
        print('Error committing files to git')
        print(out1, out2)
        exit(1)
    print('\n\t\t\033[92mPUSH SUCCESSFUL\033[0m\n')


@app.cli.command()
def syncdata():
    """
    Sync Cached DB changes in Redis to file system (DATA_DIR)
    Push changes.
    """
    while True:
        dumped_keys_length = _dump()
        if dumped_keys_length > 0:
            _push(dumped_keys_length)
        print('\t\tWAITING')
        time.sleep(5)
