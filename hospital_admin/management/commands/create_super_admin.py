
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from hospital.models import User

class Command(BaseCommand):
    help = 'Create a super admin user'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, help='Super admin username', default='superadmin')
        parser.add_argument('--email', type=str, help='Super admin email', default='superadmin@healthstack.com')
        parser.add_argument('--password', type=str, help='Super admin password', default='superadmin123')

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'Super admin with username "{username}" already exists!')
            )
            return

        user = User.objects.create(
            username=username,
            email=email,
            first_name='Super',
            last_name='Admin',
            is_super_admin=True,
            is_superuser=True,
            is_staff=True,
            password=make_password(password)
        )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created super admin: {username}')
        )
        self.stdout.write(f'Email: {email}')
        self.stdout.write(f'Password: {password}')
