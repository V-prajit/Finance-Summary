from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings
from storage.models import AdminRules, Tag
import random
import string
import os
import json

User = get_user_model()


class Command(BaseCommand):
    help = "Initialize admin account and create default admin rules"

    def handle(self, *args, **options):
        admin_username = "admin"
        admin_password = "".join(
            random.choices(string.ascii_letters + string.digits, k=16)
        )

        admin_user, created = User.objects.get_or_create(username=admin_username)
        admin_user.set_password(admin_password)
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.save()

        if settings.DEBUG:
            self.stdout.write(self.style.SUCCESS(f'Admin Password: {admin_password}'))

        json_file_path = os.path.join(settings.BASE_DIR, 'data', 'admin_tags.json')
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r') as f:
                data = json.load(f)  
            for item in data:
                tag, _ = Tag.objects.get_or_create(tag=item['tag'])
                AdminRules.objects.get_or_create(
                    name=item['name'],
                    words=item['words'],
                    match_method=item['match_method'],
                    tag=tag,
                    label=item.get('label'),
                    metadata_type=item.get('metadata_type'),
                    metadata_value=item.get('metadata_value'),
                    auto_tag=item.get('auto_tag', True)
                )   
            self.stdout.write(self.style.SUCCESS('Admin tags and rules imported successfully'))
        else:
            self.stdout.write(self.style.WARNING('admin_tags.json not found. No rules imported.'))
