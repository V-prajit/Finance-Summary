import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from storage.models import AdminRules


class Command(BaseCommand):
    help = 'Export admin-created tags and rules to a JSON file'

    def handle(self, *args, **options):
        AdminRules.export_admin_tags()
        self.stdout.write(self.style.SUCCESS('Admin tags and rules exported successfully'))