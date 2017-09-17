#
#   Import ALL Data into DB
#

import os

from django.core.management.base import BaseCommand
from django.core.management import call_command

import settings


class Command(BaseCommand):
    help = 'Import all Data from Data dir'

    def handle(self, *args, **options):

        # We have to load data in some order
        for dir in [
                    'contact',
                    'company',
                    'organization',
                    'project',
                    'sprint',
                    'deal',
                    'message',
                    'task',
                    'comment',
                    'link'
        ]:
            dir_path = os.path.abspath(os.path.join(settings.FIXTURE_DIRS[0], dir))
            print("Importing data for app :  %s" % dir)
            for root, dirs, files in os.walk(dir_path):

                for file in sorted(files):
                    path  = os.path.abspath(os.path.join(root, file))
                    call_command('loaddata', path)
