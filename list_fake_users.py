
from hospital.models import User, Patient
from doctor.models import Doctor_Information
from pharmacy.models import Pharmacist
from hospital_admin.models import Admin_Information, Clinical_Laboratory_Technician
from marketplace.models import DeliveryPartner

def list_all_fake_users():
    print("=" * 80)
    print("🔐 HEALTHSTACK SYSTEM - USER CREDENTIALS")
    print("=" * 80)
    print("🔑 Universal Password: password123")
    print("=" * 80)
    
    # Get all users
    all_users = User.objects.all().order_by('username')
    
    if not all_users:
        print("❌ No users found in the database!")
        return
    
    print(f"📊 Total Users: {all_users.count()}")
    print("=" * 80)
    
    # Organize users by type
    user_categories = {
        'patients': User.objects.filter(is_patient=True),
        'doctors': User.objects.filter(is_doctor=True),
        'hospital_admins': User.objects.filter(is_hospital_admin=True),
        'lab_workers': User.objects.filter(is_labworker=True),
        'pharmacists': User.objects.filter(is_pharmacist=True),
        'delivery_partners': User.objects.filter(is_delivery_partner=True),
    }
    
    for category, users in user_categories.items():
        if users.exists():
            print(f"\n👥 {category.upper().replace('_', ' ')} ({users.count()} users)")
            print("-" * 60)
            
            for user in users:
                # Get additional info based on user type
                additional_info = ""
                
                if category == 'patients':
                    try:
                        patient = Patient.objects.get(user=user)
                        additional_info = f" | Age: {patient.age} | Blood: {patient.blood_group}"
                    except Patient.DoesNotExist:
                        additional_info = " | Profile: Not Created"
                
                elif category == 'doctors':
                    try:
                        doctor = Doctor_Information.objects.get(user=user)
                        additional_info = f" | Dept: {doctor.department} | Fee: ৳{doctor.consultation_fee}"
                    except Doctor_Information.DoesNotExist:
                        additional_info = " | Profile: Not Created"
                
                elif category == 'pharmacists':
                    try:
                        pharmacist = Pharmacist.objects.get(user=user)
                        additional_info = f" | Degree: {pharmacist.degree} | Age: {pharmacist.age}"
                    except Pharmacist.DoesNotExist:
                        additional_info = " | Profile: Not Created"
                
                elif category == 'hospital_admins':
                    try:
                        admin = Admin_Information.objects.get(user=user)
                        hospital_name = admin.hospital.name if admin.hospital else "No Hospital"
                        additional_info = f" | Hospital: {hospital_name}"
                    except Admin_Information.DoesNotExist:
                        additional_info = " | Profile: Not Created"
                
                elif category == 'lab_workers':
                    try:
                        lab_worker = Clinical_Laboratory_Technician.objects.get(user=user)
                        hospital_name = lab_worker.hospital.name if lab_worker.hospital else "No Hospital"
                        additional_info = f" | Hospital: {hospital_name}"
                    except Clinical_Laboratory_Technician.DoesNotExist:
                        additional_info = " | Profile: Not Created"
                
                elif category == 'delivery_partners':
                    try:
                        partner = DeliveryPartner.objects.get(user=user)
                        additional_info = f" | Vehicle: {partner.vehicle_type} | Status: {partner.status}"
                    except DeliveryPartner.DoesNotExist:
                        additional_info = " | Profile: Not Created"
                
                status = "🟢 Active" if user.is_active else "🔴 Inactive"
                login_status = "🌐 Online" if user.login_status else "⚫ Offline"
                
                print(f"  📧 {user.username}")
                print(f"     Email: {user.email}")
                print(f"     Name: {user.first_name} {user.last_name}")
                print(f"     Status: {status} | {login_status}{additional_info}")
                print()
    
    print("=" * 80)
    print("🎯 QUICK LOGIN EXAMPLES:")
    print("=" * 80)
    
    # Show some quick examples
    examples = [
        ("Patient", User.objects.filter(is_patient=True).first()),
        ("Doctor", User.objects.filter(is_doctor=True).first()),
        ("Hospital Admin", User.objects.filter(is_hospital_admin=True).first()),
        ("Lab Worker", User.objects.filter(is_labworker=True).first()),
        ("Pharmacist", User.objects.filter(is_pharmacist=True).first()),
        ("Delivery Partner", User.objects.filter(is_delivery_partner=True).first()),
    ]
    
    for role, user_example in examples:
        if user_example:
            print(f"🔑 {role}: Username = {user_example.username} | Password = password123")
    
    print("=" * 80)
    print("📱 LOGIN URLS:")
    print("=" * 80)
    print("🏠 Main Login: /login/")
    print("👨‍⚕️ Doctor Login: /doctor/doctor-login/")
    print("🏥 Hospital Admin: /hospital_admin/login/")
    print("🔬 Lab Worker: /hospital_admin/login/")
    print("💊 Pharmacist: /hospital_admin/login/")
    print("=" * 80)
    
    print("✅ All user credentials listed successfully!")
    print("🔄 To regenerate data, run: python manage.py shell -c \"exec(open('generate_all_fake_data.py').read())\"")

if __name__ == '__main__':
    list_all_fake_users()
