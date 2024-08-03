import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from storage.models import AdminRules


class Command(BaseCommand):
    help = 'Export admin-created tags and rules to a JSON file'

    def handle(self, *args, **options):
        json_file_path = os.path.join(settings.BASE_DIR, 'admin_tags.json')
        if not os.path.exists(json_file_path):
            # Create an empty JSON file if it doesn't exist
            with open(json_file_path, 'w') as f:
                json.dump([], f)
            self.stdout.write(self.style.SUCCESS('Empty admin_tags.json file created'))
        else:
            # Export existing admin rules to the JSON file
            admin_rules = AdminRules.objects.all()
            data = []
            for rule in admin_rules:
                data.append({
                    'name': rule.name,
                    'pattern': rule.pattern,
                    'tag': rule.tag.tag,
                })
            
            with open(json_file_path, 'w') as f:
                json.dump(data, f, indent=4)
            
            self.stdout.write(self.style.SUCCESS('Admin tags and rules exported successfully'))