
from hospital.models import User

def list_all_fake_users():
    """List all users with their usernames and a note about the password"""
    users = User.objects.all()
    
    print("="*80)
    print("FAKE DATA USER CREDENTIALS")
    print("="*80)
    print(f"Total Users: {users.count()}")
    print("Password for ALL users: password123")
    print("="*80)
    
    # Group users by type
    user_types = {
        'Patients': users.filter(is_patient=True),
        'Doctors': users.filter(is_doctor=True),
        'Hospital Admins': users.filter(is_hospital_admin=True),
        'Lab Workers': users.filter(is_labworker=True),
        'Pharmacists': users.filter(is_pharmacist=True),
        'Delivery Partners': users.filter(is_delivery_partner=True),
    }
    
    for user_type, user_queryset in user_types.items():
        if user_queryset.exists():
            print(f"\n{user_type} ({user_queryset.count()}):")
            print("-" * 40)
            for user in user_queryset:
                print(f"Username: {user.username}")
                print(f"Email: {user.email}")
                print(f"Active: {user.is_active}")
                print("-" * 20)
    
    print("\n" + "="*80)
    print("LOGIN INSTRUCTIONS:")
    print("1. Use any username from the list above")
    print("2. Password is always: password123")
    print("3. All users are activated for testing")
    print("="*80)

if __name__ == '__main__':
    list_all_fake_users()
