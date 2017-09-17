#
#   Import ALL Data into DB
#

import os

from django.core.management.base import BaseCommand
from django.core.management import call_command
import django.apps

import settings


class Command(BaseCommand):
    help = 'Export all models data to Data dir'

    def handle(self, *args, **options):

        models = {
            'contact': ['contact', 'contactphone', 'contactemail', 'messagechannel'],
            'company': ['companyphone', 'companyemail', 'company'],
            'deal': ['deal'],
            'organization': ['organization'],
            'project': ['project'],
            'sprint': ['sprint'],
            'comment': ['comment'],
            'task': ['task', 'taskassignment', 'tasktracking'],
            'message': ['message', 'messagecontact'],
            'link': ['linklabel', 'link']

        }

        for app,  models in models.items():
            for model in models:
                dir = os.path.abspath(os.path.join(settings.FIXTURE_DIRS[0], app))
                if not os.path.exists(dir):
                    os.makedirs(dir)
                path = os.path.join(dir, '%s.json' % model)
                print('Exporting : %s' % path)
                call_command('dumpdata', '%s.%s' % (app, model), format='json', indent=4, output=path)