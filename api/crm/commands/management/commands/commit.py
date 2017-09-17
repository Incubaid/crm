#
#
#
import os
import json
from django.core.management.base import BaseCommand
from django.core.cache import cache
import settings

class Command(BaseCommand):
    help = 'Commit changes in redis'

    def handle(self, *args, **options):

        keys = cache.keys("*")
        keys.sort()
        print(keys)
        for k in keys:
            data = cache.get(k)
            cache.delete(k)
            username = data['username']
            email = data['email']
            add = data['data'].get('add', '[]')
            update = data['data'].get('update', '[]')
            delete = data['data'].get('delete', '[]')

            for entry in json.loads(add):
                import ipdb; ipdb.set_trace()
                app, model = entry['model'].split('.')
                dir = os.path.abspath(os.path.join(settings.FIXTURE_DIRS[0], app))
                path = os.path.abspath(os.path.join(dir, '%s.json' % model))

                with open(os.path.abspath(os.path.join(dir, '%s.json' % model)), 'r+') as f:
                    data = json.load(f)
                    data.append(entry)
                    json.dump(data, f)

