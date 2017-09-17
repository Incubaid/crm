#
# Clean All migration files under app/migrations
#

import os

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Clean all migrations files (Sometimes useful during development)'

    def handle(self, *args, **options):
        for root, dirs, files in os.walk("crm"):
            # We only care about app/migrations DIRS
            if not root.endswith('migrations'):
                continue
            for file in files:
                # Don't remove __init__.py
                if file == '__init__.py':
                    continue
                # Otherwise Delete file
                path = os.path.abspath(os.path.join(root, file))
                print('Deleting :%s' % path)
                os.remove(path)