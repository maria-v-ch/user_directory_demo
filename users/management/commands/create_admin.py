from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates an admin user'

    def handle(self, *args, **options):
        username = 'admin'
        email = 'admin@example.com'
        password = 'adminpassword'
        
        if not User.objects.filter(username=username).exists():
            admin_user = User.objects.create_superuser(username, email, password)
            admin_group, created = Group.objects.get_or_create(name='Admins')
            admin_user.groups.add(admin_group)
            self.stdout.write(self.style.SUCCESS(f'Admin user created - {username}'))
        else:
            self.stdout.write(self.style.WARNING('Admin user already exists'))
