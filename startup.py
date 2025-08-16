
#!/usr/bin/env python
import os
import sys
import subprocess

def run_command(command):
    """Run a command and return its result"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {command}")
            return True
        else:
            print(f"❌ {command}")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {command}")
        print(f"Exception: {e}")
        return False

def main():
    print("🚀 Starting HealthStack Setup...")
    
    # Set Django settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthstack.settings')
    
    commands = [
        "python manage.py collectstatic --noinput",
        "python manage.py migrate",
        "python manage.py setup_project",
    ]
    
    for command in commands:
        if not run_command(command):
            print("Setup failed. Please check the errors above.")
            sys.exit(1)
    
    print("✅ Setup completed successfully!")
    print("🌐 Starting server on http://0.0.0.0:5000")
    
    # Start the server
    os.system("python manage.py runserver 0.0.0.0:5000")

if __name__ == '__main__':
    main()
