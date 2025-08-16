
#!/usr/bin/env python
import os
import sys
import django
from django.conf import settings
from django.core.management import execute_from_command_line

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthstack.settings')
    django.setup()
    
    # Remove existing database
    if os.path.exists('db.sqlite3'):
        os.remove('db.sqlite3')
        print("Removed existing database")
    
    # Run migrations
    execute_from_command_line(['manage.py', 'migrate'])
    print("Database migrated successfully")
    
    # Create superuser prompt
    print("\nTo create a superuser, run: python manage.py createsuperuser")
