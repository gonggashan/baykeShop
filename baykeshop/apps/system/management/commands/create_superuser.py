from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Create a superuser with a password in non-interactive mode.'

    def handle(self, *args, **options):
        if not User.objects.filter(username='test').exists():
            User.objects.create_superuser('test', 'test@email.com', '123321')
            self.stdout.write(self.style.SUCCESS('Successfully created superuser'))
