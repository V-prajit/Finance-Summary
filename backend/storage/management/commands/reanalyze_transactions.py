from django.core.management.base import BaseCommand
from storage.models import Transaction
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Reanalyze all transactions for all users or a specific user'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, help='Username to reanalyze transactions for')

    def handle(self, *args, **options):
        if options['username']:
            try:
                user = User.objects.get(username=options['username'])
                Transaction.reanalyze_all_for_user(user)
                self.stdout.write(self.style.SUCCESS(f'Reanalyzed all transactions for user {user.username}'))
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'User {options["username"]} does not exist'))
        else:
            for user in User.objects.all():
                Transaction.reanalyze_all_for_user(user)
            self.stdout.write(self.style.SUCCESS('Reanalyzed all transactions for all users'))