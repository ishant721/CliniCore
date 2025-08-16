
import random
from datetime import timedelta, datetime
from django.utils import timezone
from faker import Faker

# Import all models from your apps
from hospital.models import User, Hospital_Information, Patient
from doctor.models import (
    Doctor_Information, Appointment, Education, Experience, Report, Specimen, Test,
    Prescription, Prescription_medicine, Prescription_test, testCart, testOrder, Doctor_review
)
from pharmacy.models import Pharmacist, Medicine, Cart, Order
from hospital_admin.models import (
    Admin_Information, Clinical_Laboratory_Technician, hospital_department,
    specialization, service, Test_Information
)
from marketplace.models import ServiceProvider, DeliveryPartner, MarketplaceOrder
from ChatApp.models import chatMessages
from sslcommerz.models import Payment

fake = Faker()

def generate_all_fake_data(num_users=50, num_hospitals=8, num_doctors_per_hospital=3,
                           num_pharmacists=5, num_lab_workers=5, num_delivery_partners=8,
                           num_medicines=40, num_tests=15, num_patients_per_user=1,
                           num_appointments_per_patient=3, num_prescriptions_per_patient=2,
                           num_marketplace_orders=15, num_chat_messages=30, num_doctor_reviews=20):
    print("🚀 Starting comprehensive fake data generation...")

    # --- Helper Functions ---
    def get_random_user(user_type=None):
        if user_type:
            if user_type == 'patient':
                return User.objects.filter(is_patient=True).order_by('?').first()
            elif user_type == 'doctor':
                return User.objects.filter(is_doctor=True).order_by('?').first()
            elif user_type == 'hospital_admin':
                return User.objects.filter(is_hospital_admin=True).order_by('?').first()
            elif user_type == 'labworker':
                return User.objects.filter(is_labworker=True).order_by('?').first()
            elif user_type == 'pharmacist':
                return User.objects.filter(is_pharmacist=True).order_by('?').first()
            elif user_type == 'delivery_partner':
                return User.objects.filter(is_delivery_partner=True).order_by('?').first()
        return User.objects.order_by('?').first()

    def get_random_hospital():
        return Hospital_Information.objects.order_by('?').first()

    def get_random_doctor():
        return Doctor_Information.objects.order_by('?').first()

    def get_random_patient():
        return Patient.objects.order_by('?').first()

    def get_random_pharmacist():
        return Pharmacist.objects.order_by('?').first()

    def get_random_lab_worker():
        return Clinical_Laboratory_Technician.objects.order_by('?').first()

    def get_random_medicine():
        return Medicine.objects.order_by('?').first()

    def get_random_test_information():
        return Test_Information.objects.order_by('?').first()

    def get_random_service_provider(service_type=None):
        if service_type:
            return ServiceProvider.objects.filter(service_type=service_type).order_by('?').first()
        return ServiceProvider.objects.order_by('?').first()

    def get_random_delivery_partner():
        return DeliveryPartner.objects.order_by('?').first()

    # --- Clear Existing Data ---
    print("🗑️ Clearing existing data...")
    Payment.objects.all().delete()
    MarketplaceOrder.objects.all().delete()
    chatMessages.objects.all().delete()
    Doctor_review.objects.all().delete()
    testOrder.objects.all().delete()
    testCart.objects.all().delete()
    Prescription_medicine.objects.all().delete()
    Prescription_test.objects.all().delete()
    Prescription.objects.all().delete()
    Appointment.objects.all().delete()
    Education.objects.all().delete()
    Experience.objects.all().delete()
    Report.objects.all().delete()
    Specimen.objects.all().delete()
    Test.objects.all().delete()
    Cart.objects.all().delete()
    Order.objects.all().delete()
    Doctor_Information.objects.all().delete()
    Pharmacist.objects.all().delete()
    Clinical_Laboratory_Technician.objects.all().delete()
    Admin_Information.objects.all().delete()
    Patient.objects.all().delete()
    ServiceProvider.objects.all().delete()
    DeliveryPartner.objects.all().delete()
    hospital_department.objects.all().delete()
    specialization.objects.all().delete()
    service.objects.all().delete()
    Test_Information.objects.all().delete()
    Medicine.objects.all().delete()
    Hospital_Information.objects.all().delete()
    User.objects.all().delete()

    # --- 1. Generate Users ---
    print("👥 Generating Users...")
    users = []
    user_types = ['patient', 'doctor', 'hospital_admin', 'labworker', 'pharmacist', 'delivery_partner']
    
    for i in range(num_users):
        username = f"user{i+1}_{fake.user_name()}"[:30]
        email = f"user{i+1}@{fake.domain_name()}"
        password = "password123"

        user = User.objects.create_user(
            username=username, 
            email=email, 
            password=password,
            first_name=fake.first_name(),
            last_name=fake.last_name()
        )
        
        # Assign random user types
        user_type_choice = random.choice(user_types)
        if user_type_choice == 'patient':
            user.is_patient = True
        elif user_type_choice == 'doctor':
            user.is_doctor = True
        elif user_type_choice == 'hospital_admin':
            user.is_hospital_admin = True
        elif user_type_choice == 'labworker':
            user.is_labworker = True
        elif user_type_choice == 'pharmacist':
            user.is_pharmacist = True
        elif user_type_choice == 'delivery_partner':
            user.is_delivery_partner = True
        
        user.is_active = True
        user.login_status = fake.boolean()
        user.save()
        users.append(user)
        print(f"  ✅ Created User: {user.username} ({user_type_choice})")

    # --- 2. Generate Hospital_Information ---
    print("🏥 Generating Hospitals...")
    hospitals = []
    hospital_names = [
        "City General Hospital", "Metropolitan Medical Center", "Sacred Heart Hospital",
        "St. Mary's Medical Complex", "Regional Health Center", "University Hospital",
        "Children's Hospital", "Heart & Vascular Institute"
    ]
    
    for i in range(num_hospitals):
        lat = round(random.uniform(23.7, 23.9), 6)
        lon = round(random.uniform(90.3, 90.5), 6)
        
        hospital = Hospital_Information.objects.create(
            name=hospital_names[i % len(hospital_names)] if i < len(hospital_names) else f"{fake.company()} Hospital",
            address=fake.address(),
            featured_image='hospitals/default.png',
            description=fake.paragraph(),
            email=f"info@hospital{i+1}.com",
            phone_number=random.randint(1000000000, 9999999999),
            hospital_type=random.choice(['public', 'private']),
            general_bed_no=random.randint(50, 500),
            available_icu_no=random.randint(5, 50),
            regular_cabin_no=random.randint(10, 100),
            emergency_cabin_no=random.randint(5, 50),
            vip_cabin_no=random.randint(1, 10),
            latitude=lat,
            longitude=lon
        )
        hospitals.append(hospital)
        print(f"  🏥 Created Hospital: {hospital.name}")

    # --- 3. Generate hospital admin related data ---
    print("🏢 Generating Hospital Admin Related Data...")
    departments = []
    specializations_list = []
    services = []

    dept_names = [
        'Cardiology', 'Neurology', 'Pediatrics', 'Orthopedics', 'Dermatology',
        'Gastroenterology', 'Psychiatry', 'Radiology', 'Emergency Medicine',
        'Internal Medicine', 'Surgery', 'Oncology', 'Urology', 'ENT', 'Gynecology'
    ]

    spec_names = [
        'Interventional Cardiology', 'Pediatric Neurology', 'Orthopedic Surgery',
        'Cosmetic Dermatology', 'Gastroenterology', 'Child Psychiatry',
        'Emergency Medicine', 'General Surgery', 'Medical Oncology',
        'Urological Surgery', 'Head and Neck Surgery', 'Obstetrics'
    ]

    service_names = [
        'Emergency Services', 'Laboratory Services', 'Radiology Services',
        'Pharmacy Services', 'Blood Bank', 'ICU Services', 'Operation Theater',
        'Ambulance Services', 'Home Care Services', 'Telemedicine'
    ]

    for hospital in hospitals:
        # Create departments
        for dept_name in random.sample(dept_names, random.randint(5, 8)):
            dept = hospital_department.objects.create(
                hospital_department_name=dept_name,
                hospital=hospital,
                featured_image='departments/default.png'
            )
            departments.append(dept)
        
        # Create specializations
        for spec_name in random.sample(spec_names, random.randint(4, 7)):
            spec = specialization.objects.create(
                specialization_name=spec_name,
                hospital=hospital
            )
            specializations_list.append(spec)

        # Create services
        for service_name in random.sample(service_names, random.randint(4, 6)):
            serv = service.objects.create(
                service_name=service_name,
                hospital=hospital
            )
            services.append(serv)

    print(f"  📋 Created {len(departments)} departments, {len(specializations_list)} specializations, {len(services)} services.")

    # --- 4. Generate Test_Information ---
    print("🧪 Generating Test Information...")
    test_info_list = []
    test_names = [
        'Complete Blood Count', 'Lipid Profile', 'Liver Function Test', 'Kidney Function Test',
        'Thyroid Function Test', 'Blood Sugar (Fasting)', 'HbA1c', 'Chest X-Ray',
        'ECG', 'Echocardiogram', 'CT Scan Head', 'MRI Brain', 'Ultrasound Abdomen',
        'Urine Analysis', 'Stool Analysis'
    ]
    
    for test_name in test_names:
        test_info = Test_Information.objects.create(
            test_name=test_name,
            test_price=str(random.randint(200, 5000))
        )
        test_info_list.append(test_info)
        print(f"  🧪 Created Test Info: {test_info.test_name}")

    # --- 5. Generate Admin_Information ---
    print("👔 Generating Admin Information...")
    admin_users = User.objects.filter(is_hospital_admin=True)
    for user in admin_users:
        hospital = random.choice(hospitals) if hospitals else None
        Admin_Information.objects.create(
            user=user,
            name=f"{user.first_name} {user.last_name}",
            username=user.username,
            email=user.email,
            phone_number=f"01{random.randint(700000000, 999999999)}",
            role='hospital',
            hospital=hospital
        )
        print(f"  👔 Created Admin Information for: {user.username}")

    # --- 6. Generate Doctor_Information ---
    print("👨‍⚕️ Generating Doctors...")
    doctors = []
    doctor_users = User.objects.filter(is_doctor=True)
    
    for user in doctor_users:
        hospital = random.choice(hospitals) if hospitals else None
        department = random.choice(departments) if departments else None
        specialization_obj = random.choice(specializations_list) if specializations_list else None

        if not hospital or not department or not specialization_obj:
            print(f"  ⚠️ Skipping doctor creation for {user.username}: Missing related data.")
            continue

        lat = float(hospital.latitude) + random.uniform(-0.05, 0.05)
        lon = float(hospital.longitude) + random.uniform(-0.05, 0.05)

        doctor = Doctor_Information.objects.create(
            user=user,
            name=f"{user.first_name} {user.last_name}",
            username=user.username,
            gender=random.choice(['Male', 'Female']),
            description=fake.paragraph(),
            department=random.choice(['Cardiologists', 'Neurologists', 'Pediatricians', 'Physiatrists', 'Dermatologists']),
            department_name=department,
            specialization=specialization_obj,
            featured_image='doctors/user-default.png',
            certificate_image='doctors_certificate/default.png',
            email=user.email,
            phone_number=f"01{random.randint(700000000, 999999999)}",
            nid=f"{random.randint(1000000000000, 9999999999999)}",
            visiting_hour=random.choice(['9:00 AM - 5:00 PM', '2:00 PM - 8:00 PM', '10:00 AM - 6:00 PM']),
            consultation_fee=random.randint(800, 3000),
            report_fee=random.randint(300, 1500),
            dob=fake.date_of_birth(minimum_age=28, maximum_age=65).strftime('%Y-%m-%d'),
            register_status='Accepted',
            hospital_name=hospital,
            latitude=lat,
            longitude=lon,
            is_marketplace_active=fake.boolean(),
            home_visit_available=fake.boolean(),
            online_consultation_available=True,
            instant_booking_available=fake.boolean(),
            service_radius=random.randint(5, 50),
            home_visit_fee=random.randint(1500, 4000) if fake.boolean() else None,
            online_consultation_fee=random.randint(600, 2000) if fake.boolean() else None,
            average_response_time=random.randint(10, 90),
            marketplace_rating=round(random.uniform(3.5, 5.0), 2),
            total_marketplace_reviews=random.randint(5, 250),
            total_consultations=random.randint(20, 1200)
        )
        doctors.append(doctor)
        print(f"  👨‍⚕️ Created Doctor: {doctor.name}")

    # --- 7. Generate Education and Experience for Doctors ---
    print("🎓 Generating Doctor Education and Experience...")
    degree_list = [
        "MBBS", "MBBS, MD", "MBBS, FCPS", "MBBS, MS", "MBBS, PhD",
        "BDS", "BAMS", "BHMS", "MBBS, DM", "MBBS, MCh"
    ]
    
    institute_list = [
        "Dhaka Medical College", "Chittagong Medical College", "Sylhet MAG Osmani Medical College",
        "Rajshahi Medical College", "Mymensingh Medical College", "Rangpur Medical College"
    ]
    
    for doctor in doctors:
        # Education
        for _ in range(random.randint(1, 3)):
            Education.objects.create(
                doctor=doctor,
                degree=random.choice(degree_list),
                institute=random.choice(institute_list),
                year_of_completion=str(random.randint(2000, 2020))
            )
        
        # Experience
        for _ in range(random.randint(1, 4)):
            start_year = random.randint(2010, 2020)
            end_year = random.randint(start_year + 1, 2024)
            Experience.objects.create(
                doctor=doctor,
                work_place_name=f"{random.choice(hospitals).name if hospitals else fake.company()}",
                from_year=str(start_year),
                to_year=str(end_year),
                designation=random.choice(['Consultant', 'Assistant Professor', 'Associate Professor', 'Registrar'])
            )
        print(f"  🎓 Added education/experience for Dr. {doctor.name}")

    # --- 8. Generate Pharmacists ---
    print("💊 Generating Pharmacists...")
    pharmacists = []
    pharmacist_users = User.objects.filter(is_pharmacist=True)
    
    for user in pharmacist_users:
        pharmacist = Pharmacist.objects.create(
            user=user,
            name=f"{user.first_name} {user.last_name}",
            username=user.username,
            degree=random.choice(['B.Pharm', 'PharmD', 'M.Pharm', 'D.Pharm']),
            featured_image='pharmacist/user-default.png',
            email=user.email,
            phone_number=random.randint(1700000000, 1999999999),
            age=random.randint(25, 60)
        )
        pharmacists.append(pharmacist)
        print(f"  💊 Created Pharmacist: {pharmacist.name}")

    # --- 9. Generate Clinical_Laboratory_Technicians ---
    print("🔬 Generating Lab Workers...")
    lab_workers = []
    labworker_users = User.objects.filter(is_labworker=True)
    
    for user in labworker_users:
        hospital = random.choice(hospitals) if hospitals else None
        if not hospital:
            print(f"  ⚠️ Skipping lab worker creation for {user.username}: No hospitals available.")
            continue
            
        lab_worker = Clinical_Laboratory_Technician.objects.create(
            user=user,
            name=f"{user.first_name} {user.last_name}",
            username=user.username,
            age=random.randint(22, 55),
            email=user.email,
            phone_number=random.randint(1700000000, 1999999999),
            featured_image='technician/user-default.png',
            hospital=hospital
        )
        lab_workers.append(lab_worker)
        print(f"  🔬 Created Lab Worker: {lab_worker.name}")

    # --- 10. Generate DeliveryPartners ---
    print("🚚 Generating Delivery Partners...")
    delivery_partners = []
    delivery_partner_users = User.objects.filter(is_delivery_partner=True)
    
    for user in delivery_partner_users:
        delivery_partner = DeliveryPartner.objects.create(
            user=user,
            name=f"{user.first_name} {user.last_name}",
            phone_number=f"01{random.randint(700000000, 999999999)}",
            vehicle_type=random.choice(['Motorcycle', 'Bicycle', 'Car', 'Van']),
            license_number=fake.license_plate(),
            current_latitude=fake.latitude(),
            current_longitude=fake.longitude(),
            status=random.choice(['available', 'busy', 'offline']),
            is_verified=fake.boolean(),
            rating=round(random.uniform(3.0, 5.0), 2),
            total_deliveries=random.randint(0, 1500)
        )
        delivery_partners.append(delivery_partner)
        print(f"  🚚 Created Delivery Partner: {delivery_partner.name}")

    # --- 11. Generate Medicines ---
    print("💉 Generating Medicines...")
    medicines = []
    medicine_names = [
        'Paracetamol', 'Ibuprofen', 'Aspirin', 'Cetirizine', 'Omeprazole',
        'Metformin', 'Lisinopril', 'Atorvastatin', 'Levothyroxine', 'Salbutamol',
        'Prednisolone', 'Diclofenac', 'Ranitidine', 'Ciprofloxacin', 'Azithromycin',
        'Cough Syrup', 'Vitamin D3', 'Calcium Tablets', 'Iron Tablets', 'Multivitamin'
    ]
    
    for medicine_name in medicine_names:
        medicine = Medicine.objects.create(
            medicine_id=f"MED{random.randint(1000, 9999)}",
            name=f"{medicine_name} {random.choice(['Tablet', 'Capsule', 'Syrup', 'Injection'])}",
            generic_name=medicine_name,
            manufacturer=fake.company(),
            weight=f"{random.randint(10, 500)}mg",
            quantity=random.randint(10, 100),
            featured_image='medicines/default.png',
            description=fake.paragraph(),
            medicine_type=random.choice(['tablets', 'syrup', 'capsule', 'general']),
            medicine_category=random.choice([
                'fever', 'pain', 'cough', 'cold', 'flu', 'diabetes', 'eye', 'ear',
                'allergy', 'asthma', 'bloodpressure', 'heartdisease', 'vitamins',
                'digestivehealth', 'skin', 'infection', 'nurological'
            ]),
            price=random.randint(20, 2000),
            stock_quantity=random.randint(0, 1000),
            Prescription_reqiuired=random.choice(['yes', 'no']),
            is_delivery_available=True,
            delivery_time_minutes=random.randint(30, 180),
            is_emergency_available=fake.boolean(),
            storage_temperature=random.choice(['Room Temperature', 'Refrigerated', 'Controlled']),
            is_marketplace_active=True,
            supplier_name=fake.company()
        )
        medicines.append(medicine)
        print(f"  💉 Created Medicine: {medicine.name}")

    # --- 12. Generate ServiceProviders ---
    print("🏪 Generating Service Providers...")
    service_providers = []
    service_types = ['consultation', 'medicine_delivery', 'lab_service', 'home_visit']
    
    for _ in range(20):
        provider_type = random.choice(service_types)
        
        hospital_obj = None
        doctor_obj = None
        pharmacist_obj = None
        name = ""
        
        if provider_type == 'consultation' and doctors:
            doctor_obj = random.choice(doctors)
            name = f"Dr. {doctor_obj.name} Consultation"
            lat = doctor_obj.latitude
            lon = doctor_obj.longitude
        elif provider_type == 'medicine_delivery' and pharmacists:
            pharmacist_obj = random.choice(pharmacists)
            name = f"{pharmacist_obj.name} Pharmacy"
            hospital_for_pharmacy = random.choice(hospitals) if hospitals else None
            lat = hospital_for_pharmacy.latitude if hospital_for_pharmacy else fake.latitude()
            lon = hospital_for_pharmacy.longitude if hospital_for_pharmacy else fake.longitude()
        elif provider_type == 'lab_service' and hospitals:
            hospital_obj = random.choice(hospitals)
            name = f"{hospital_obj.name} Lab Service"
            lat = hospital_obj.latitude
            lon = hospital_obj.longitude
        elif provider_type == 'home_visit' and doctors:
            doctor_obj = random.choice(doctors)
            name = f"Dr. {doctor_obj.name} Home Visit"
            lat = doctor_obj.latitude
            lon = doctor_obj.longitude
        else:
            name = f"{fake.company()} Healthcare Service"
            lat = fake.latitude()
            lon = fake.longitude()

        if name:
            sp = ServiceProvider.objects.create(
                name=name,
                service_type=provider_type,
                hospital=hospital_obj,
                doctor=doctor_obj,
                pharmacist=pharmacist_obj,
                latitude=lat,
                longitude=lon,
                service_radius=random.randint(5, 100),
                availability_status=random.choice(['available', 'busy', 'offline']),
                average_delivery_time=random.randint(15, 180),
                rating=round(random.uniform(3.0, 5.0), 2),
                total_reviews=random.randint(0, 500),
                base_fee=random.randint(50, 500),
                delivery_fee=random.randint(20, 150),
                emergency_fee=random.randint(50, 300)
            )
            service_providers.append(sp)
            print(f"  🏪 Created Service Provider: {sp.name}")

    # --- 13. Generate Patients ---
    print("🤒 Generating Patients...")
    patients = []
    patient_users = User.objects.filter(is_patient=True)
    
    for user in patient_users:
        for _ in range(num_patients_per_user):
            patient = Patient.objects.create(
                user=user,
                name=f"{user.first_name} {user.last_name}",
                username=user.username,
                age=random.randint(1, 90),
                email=user.email,
                phone_number=f"01{random.randint(700000000, 999999999)}",
                address=fake.address(),
                featured_image='patients/user-default.png',
                blood_group=random.choice(['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']),
                history=random.choice([
                    'No significant history', 'Hypertension', 'Diabetes Type 2', 
                    'Asthma', 'Allergies', 'Heart Disease', 'Kidney Disease'
                ]),
                dob=fake.date_of_birth(minimum_age=1, maximum_age=90).strftime('%Y-%m-%d'),
                nid=f"{random.randint(1000000000000, 9999999999999)}",
                serial_number=f"P{random.randint(10000, 99999)}",
                login_status=random.choice(['online', 'offline'])
            )
            patients.append(patient)
            print(f"  🤒 Created Patient: {patient.name}")

    # --- 14. Generate Appointments ---
    print("📅 Generating Appointments...")
    appointments = []
    for _ in range(num_appointments_per_patient * len(patients)):
        patient = random.choice(patients) if patients else None
        doctor = random.choice(doctors) if doctors else None
        
        if not patient or not doctor:
            continue
        
        appointment_date = fake.date_between(start_date="-60d", end_date="+60d")
        appointment_time = f"{random.randint(9, 17)}:{random.choice(['00', '30'])}"
        
        appointment = Appointment.objects.create(
            date=appointment_date,
            time=appointment_time,
            doctor=doctor,
            patient=patient,
            appointment_type=random.choice(['report', 'checkup']),
            appointment_status=random.choice(['pending', 'confirmed', 'cancelled']),
            serial_number=f"A{random.randint(1000, 9999)}",
            payment_status=random.choice(['pending', 'paid', 'failed']),
            transaction_id=f"TXN{random.randint(100000, 999999)}" if fake.boolean() else None,
            message=random.choice([
                'Regular checkup', 'Follow-up visit', 'Emergency consultation', 
                'Routine examination', 'Health screening'
            ])
        )
        appointments.append(appointment)
        print(f"  📅 Created Appointment for {patient.name} with Dr. {doctor.name}")

    # --- 15. Generate Reports, Specimens, and Tests ---
    print("📊 Generating Reports, Specimens, and Tests...")
    reports = []
    for _ in range(len(patients) * 2):
        patient = random.choice(patients) if patients else None
        doctor = random.choice(doctors) if doctors else None
        lab_worker = random.choice(lab_workers) if lab_workers else None
        
        if not patient or not doctor:
            continue
        
        report = Report.objects.create(
            doctor=doctor,
            patient=patient,
            lab_technician=lab_worker,
            specimen_id=f"SPEC{random.randint(1000, 9999)}",
            specimen_type=random.choice(['Blood', 'Urine', 'Tissue', 'Sputum']),
            collection_date=fake.date_this_year().strftime('%Y-%m-%d'),
            receiving_date=fake.date_this_year().strftime('%Y-%m-%d'),
            test_name=random.choice(['CBC', 'Lipid Profile', 'LFT', 'KFT', 'Thyroid Panel']),
            result=random.choice(['Normal', 'Abnormal', 'High', 'Low', 'Borderline']),
            unit=random.choice(['mg/dL', 'g/L', 'cells/mL', 'IU/L', 'ng/mL']),
            referred_value=f"{random.randint(10, 100)}-{random.randint(101, 200)}",
            delivery_date=fake.date_this_year().strftime('%Y-%m-%d'),
            other_information=fake.sentence() if fake.boolean() else None,
            created_at=timezone.now(),
            updated_at=timezone.now()
        )
        reports.append(report)

        # Add specimens and tests for each report
        for _ in range(random.randint(1, 3)):
            Specimen.objects.create(
                report=report,
                specimen_type=random.choice(['Blood', 'Urine', 'Tissue']),
                collection_date=fake.date_this_year().strftime('%Y-%m-%d'),
                receiving_date=fake.date_this_year().strftime('%Y-%m-%d')
            )
        
        for _ in range(random.randint(1, 5)):
            Test.objects.create(
                report=report,
                test_name=f"{random.choice(['CBC', 'Glucose', 'Creatinine', 'ALT', 'TSH'])} Test",
                result=random.choice(['Normal', 'High', 'Low', 'Critical']),
                unit=random.choice(['mg/dL', 'g/L', 'IU/L']),
                referred_value=f"{random.randint(10, 50)}-{random.randint(51, 100)}"
            )
        print(f"  📊 Created Report for {patient.name}")

    # --- 16. Generate Prescriptions ---
    print("📝 Generating Prescriptions...")
    prescriptions = []
    for _ in range(num_prescriptions_per_patient * len(patients)):
        patient = random.choice(patients) if patients else None
        doctor = random.choice(doctors) if doctors else None
        
        if not patient or not doctor:
            continue
        
        prescription = Prescription.objects.create(
            doctor=doctor,
            patient=patient,
            create_date=fake.date_this_year().strftime('%Y-%m-%d'),
            medicine_name=random.choice(['Paracetamol', 'Ibuprofen', 'Aspirin']),
            quantity=str(random.randint(10, 30)),
            days=str(random.randint(5, 30)),
            time=random.choice(['Morning', 'Afternoon', 'Evening', '3 times daily']),
            relation_with_meal=random.choice(['Before Meal', 'After Meal', 'With Meal']),
            medicine_description=fake.sentence(),
            test_name=random.choice(['Blood Test', 'Urine Test', 'X-Ray', 'None']),
            test_description=fake.sentence(),
            extra_information=fake.paragraph() if fake.boolean() else None
        )
        prescriptions.append(prescription)

        # Create prescription medicines
        for _ in range(random.randint(1, 4)):
            Prescription_medicine.objects.create(
                prescription=prescription,
                medicine_name=f"{random.choice(['Paracetamol', 'Ibuprofen', 'Aspirin'])} {random.choice(['500mg', '200mg', '100mg'])}",
                quantity=str(random.randint(10, 30)),
                duration=f"{random.randint(5, 30)} days",
                frequency=random.choice(['Once Daily', 'Twice Daily', 'Thrice Daily']),
                relation_with_meal=random.choice(['Before Meal', 'After Meal', 'With Meal']),
                instruction=fake.sentence(),
                is_ordered=fake.boolean(),
                order_status=random.choice(['pending', 'ordered', 'delivered', 'cancelled']),
                ordered_date=timezone.now() if fake.boolean() else None
            )
        
        # Create prescription tests
        for _ in range(random.randint(0, 2)):
            test_info = random.choice(test_info_list) if test_info_list else None
            if test_info:
                Prescription_test.objects.create(
                    prescription=prescription,
                    test_name=test_info.test_name,
                    test_description=fake.sentence(),
                    test_info_id=test_info.test_id,
                    test_info_price=test_info.test_price,
                    test_info_pay_status=random.choice(['Paid', 'Unpaid'])
                )
        print(f"  📝 Created Prescription for {patient.name}")

    # Continue with additional data generation...
    print("🛒 Generating Cart and Orders...")
    # Generate cart items and orders for pharmacy
    for patient in patients[:20]:  # Limit to first 20 patients
        if random.random() < 0.6:  # 60% chance
            cart_items = []
            for _ in range(random.randint(1, 4)):
                medicine = random.choice(medicines) if medicines else None
                if medicine:
                    cart_item = Cart.objects.create(
                        user=patient.user,
                        item=medicine,
                        quantity=random.randint(1, 5),
                        purchased=True
                    )
                    cart_items.append(cart_item)
            
            if cart_items:
                order = Order.objects.create(
                    user=patient.user,
                    ordered=True,
                    created=timezone.now(),
                    payment_status=random.choice(['paid', 'pending', 'failed']),
                    trans_ID=f"ORD{random.randint(100000, 999999)}"
                )
                order.orderitems.set(cart_items)
                print(f"  🛒 Created Order for {patient.name}")

    print("🧪 Generating Test Orders...")
    # Generate test cart and orders
    for patient in patients[:15]:  # Limit to first 15 patients
        if random.random() < 0.4:  # 40% chance
            test_cart_items = []
            for _ in range(random.randint(1, 2)):
                prescription_test = Prescription_test.objects.order_by('?').first()
                if prescription_test:
                    test_cart_item = testCart.objects.create(
                        user=patient.user,
                        item=prescription_test,
                        name=prescription_test.test_name,
                        purchased=True
                    )
                    test_cart_items.append(test_cart_item)
            
            if test_cart_items:
                test_order = testOrder.objects.create(
                    user=patient.user,
                    ordered=True,
                    created=timezone.now(),
                    payment_status=random.choice(['paid', 'pending', 'failed']),
                    trans_ID=f"TEST{random.randint(100000, 999999)}"
                )
                test_order.orderitems.set(test_cart_items)
                print(f"  🧪 Created Test Order for {patient.name}")

    print("💰 Generating Payments...")
    # Generate payments
    for _ in range(30):
        patient = random.choice(patients) if patients else None
        if not patient:
            continue
        
        payment_type = random.choice(['appointment', 'medicine', 'lab_test'])
        
        appointment_obj = None
        order_obj = None
        test_order_obj = None
        prescription_obj = None

        if payment_type == 'appointment':
            appointment_obj = Appointment.objects.filter(patient=patient).order_by('?').first()
        elif payment_type == 'medicine':
            order_obj = Order.objects.filter(user=patient.user).order_by('?').first()
        elif payment_type == 'lab_test':
            test_order_obj = testOrder.objects.filter(user=patient.user).order_by('?').first()
        
        prescription_obj = Prescription.objects.filter(patient=patient).order_by('?').first()

        Payment.objects.create(
            invoice_number=f"INV{random.randint(10000, 99999)}",
            patient=patient,
            appointment=appointment_obj,
            order=order_obj,
            test_order=test_order_obj,
            prescription=prescription_obj,
            payment_type=payment_type,
            name=patient.name,
            email=patient.email,
            phone=patient.phone_number,
            address=patient.address,
            city=fake.city(),
            country='Bangladesh',
            transaction_id=f"TXN{random.randint(100000, 999999)}",
            val_transaction_id=f"VAL{random.randint(100000, 999999)}",
            currency_amount=str(random.randint(100, 5000)),
            consulation_fee=str(random.randint(500, 2000)) if random.random() < 0.5 else None,
            report_fee=str(random.randint(200, 1000)) if random.random() < 0.5 else None,
            card_type=random.choice(['VISA', 'MasterCard', 'American Express']) if fake.boolean() else None,
            card_no=fake.credit_card_number() if fake.boolean() else None,
            bank_transaction_id=f"BANK{random.randint(100000, 999999)}" if fake.boolean() else None,
            status=random.choice(['VALID', 'FAILED', 'PENDING']),
            transaction_date=timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
            currency='BDT',
            card_issuer=fake.company() if fake.boolean() else None,
            card_brand=fake.credit_card_provider() if fake.boolean() else None
        )
        print(f"  💰 Created Payment for {patient.name}")

    print("🛍️ Generating Marketplace Orders...")
    # Generate marketplace orders
    for _ in range(num_marketplace_orders):
        user = random.choice(users) if users else None
        service_provider = random.choice(service_providers) if service_providers else None
        delivery_partner = random.choice(delivery_partners) if delivery_partners and fake.boolean() else None
        
        if not user or not service_provider:
            continue

        MarketplaceOrder.objects.create(
            user=user,
            service_provider=service_provider,
            delivery_partner=delivery_partner,
            order_type=service_provider.service_type,
            status=random.choice(['pending', 'confirmed', 'in_progress', 'completed', 'cancelled']),
            priority=random.choice(['low', 'medium', 'high', 'urgent']),
            delivery_latitude=fake.latitude(),
            delivery_longitude=fake.longitude(),
            delivery_address=fake.address(),
            subtotal=random.randint(100, 3000),
            delivery_fee=random.randint(50, 200),
            total_amount=random.randint(200, 3200),
            estimated_delivery_time=timezone.now() + timedelta(hours=random.randint(1, 4)),
            actual_delivery_time=timezone.now() + timedelta(hours=random.randint(1, 6)) if fake.boolean() else None,
            payment_status=random.choice(['paid', 'pending', 'failed']),
            transaction_id=f"MP{random.randint(100000, 999999)}" if fake.boolean() else None
        )
        print(f"  🛍️ Created Marketplace Order for {user.username}")

    print("💬 Generating Chat Messages...")
    # Generate chat messages
    all_users = list(User.objects.all())
    if len(all_users) >= 2:
        for _ in range(num_chat_messages):
            user1 = random.choice(all_users)
            user2 = random.choice(all_users)
            while user1 == user2:
                user2 = random.choice(all_users)
            
            chatMessages.objects.create(
                user_from=user1,
                user_to=user2,
                message=fake.sentence(),
                date_created=timezone.now()
            )
            print(f"  💬 Created Chat Message between {user1.username} and {user2.username}")

    print("⭐ Generating Doctor Reviews...")
    # Generate doctor reviews
    for _ in range(num_doctor_reviews):
        doctor = random.choice(doctors) if doctors else None
        patient = random.choice(patients) if patients else None
        
        if not doctor or not patient:
            continue
        
        Doctor_review.objects.create(
            doctor=doctor,
            patient=patient,
            title=fake.sentence(nb_words=4),
            message=fake.paragraph()
        )
        print(f"  ⭐ Created Review for Dr. {doctor.name}")

    print("✅ Comprehensive fake data generation complete!")
    print(f"""
📊 Generated Data Summary:
👥 Users: {User.objects.count()}
🏥 Hospitals: {Hospital_Information.objects.count()}
👨‍⚕️ Doctors: {Doctor_Information.objects.count()}
🤒 Patients: {Patient.objects.count()}
💊 Pharmacists: {Pharmacist.objects.count()}
🔬 Lab Workers: {Clinical_Laboratory_Technician.objects.count()}
🚚 Delivery Partners: {DeliveryPartner.objects.count()}
💉 Medicines: {Medicine.objects.count()}
📅 Appointments: {Appointment.objects.count()}
📝 Prescriptions: {Prescription.objects.count()}
📊 Reports: {Report.objects.count()}
💰 Payments: {Payment.objects.count()}
🛍️ Marketplace Orders: {MarketplaceOrder.objects.count()}
💬 Chat Messages: {chatMessages.objects.count()}
⭐ Doctor Reviews: {Doctor_review.objects.count()}
    """)

if __name__ == '__main__':
    generate_all_fake_data()
