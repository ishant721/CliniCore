
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from hospital.models import Hospital_Information

User = get_user_model()

class Command(BaseCommand):
    help = 'Setup initial project data'

    def handle(self, *args, **options):
        # Create superuser if none exists
        if not User.objects.filter(is_superuser=True).exists():
            self.stdout.write('Creating superuser...')
            User.objects.create_superuser(
                username='admin',
                email='admin@healthstack.com',
                password='admin123',
                first_name='Admin',
                last_name='User'
            )
            self.stdout.write(self.style.SUCCESS('Superuser created successfully'))
        
        self.stdout.write(self.style.SUCCESS('Project setup completed!'))
