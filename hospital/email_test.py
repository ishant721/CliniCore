
from django.core.mail import send_mail
from django.conf import settings

def test_email_configuration():
    """Test function to verify email configuration"""
    try:
        send_mail(
            'Test Email - HealthStack',
            'This is a test email to verify SMTP configuration is working correctly.',
            settings.DEFAULT_FROM_EMAIL,
            ['ishantsingh01275@gmail.com'],  # Send to yourself for testing
            fail_silently=False,
        )
        print("✅ Email sent successfully!")
        return True
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return False

if __name__ == "__main__":
    import django
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthstack.settings')
    django.setup()
    test_email_configuration()
