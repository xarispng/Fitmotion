from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Hash passwords for users loaded from fixtures'

    def handle(self, *args, **options):
        call_command('loaddata', 'initial_users')

        users = User.objects.all()
        for user in users:
            user.password = make_password(user.password)
            user.save()
        self.stdout.write(self.style.SUCCESS('Successfully hashed passwords for all users'))