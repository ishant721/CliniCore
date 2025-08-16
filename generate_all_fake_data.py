import random
from datetime import timedelta
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

def generate_all_fake_data(num_users=50, num_hospitals=5, num_doctors_per_hospital=3,
                           num_pharmacists=3, num_lab_workers=3, num_delivery_partners=5,
                           num_medicines=30, num_tests=10, num_patients_per_user=1,
                           num_appointments_per_patient=2, num_prescriptions_per_patient=1,
                           num_marketplace_orders=10, num_chat_messages=20, num_doctor_reviews=15):
    print("Starting comprehensive fake data generation...")

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

    # --- Clear Existing Data (Optional - uncomment with caution!) ---
    print("Clearing existing data...")
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
    Hospital_Information.objects.all().delete()
    User.objects.all().delete() # BE VERY CAREFUL WITH THIS ONE!

    # --- 1. Generate Users ---
    print("Generating Users...")
    users = []
    for i in range(num_users):
        username = fake.user_name() + str(i)
        email = fake.email()
        password = "password123" # Simple password for all fake users

        user = User.objects.create_user(username=username, email=email, password=password)
        
        # Assign random user types
        user_type_choice = random.choice(['patient', 'doctor', 'hospital_admin', 'labworker', 'pharmacist', 'delivery_partner'])
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
        
        user.is_active = True # Activate all for testing purposes
        user.save()
        users.append(user)
        print(f"  Created User: {user.username} ({user_type_choice})")

    # --- 2. Generate Hospital_Information ---
    print("Generating Hospitals...")
    hospitals = []
    for _ in range(num_hospitals):
        lat = fake.latitude()
        lon = fake.longitude()
        hospital = Hospital_Information.objects.create(
            name=fake.company() + " Hospital",
            address=fake.address(),
            featured_image='hospitals/default.png',
            description=fake.paragraph(),
            email=fake.company_email(),
            phone_number=random.randint(1000000000, 9999999999),
            hospital_type=random.choice([choice[0] for choice in Hospital_Information.HOSPITAL_TYPE]),
            general_bed_no=random.randint(50, 500),
            available_icu_no=random.randint(5, 50),
            regular_cabin_no=random.randint(10, 100),
            emergency_cabin_no=random.randint(5, 50),
            vip_cabin_no=random.randint(1, 10),
            latitude=lat,
            longitude=lon
        )
        hospitals.append(hospital)
        print(f"  Created Hospital: {hospital.name} ({lat}, {lon})")

    # --- 3. Generate hospital_admin_related (Departments, Specializations, Services) ---
    print("Generating Hospital Admin Related Data (Departments, Specializations, Services)...")
    departments = []
    specializations = []
    services = []

    for hospital in hospitals:
        for _ in range(random.randint(2, 5)): # 2-5 departments per hospital
            dept = hospital_department.objects.create(
                hospital_department_name=fake.word().capitalize() + " Department",
                hospital=hospital,
                featured_image='departments/default.png'
            )
            departments.append(dept)
        
        for _ in range(random.randint(3, 7)): # 3-7 specializations per hospital
            spec = specialization.objects.create(
                specialization_name=fake.job() + " Specialist",
                hospital=hospital
            )
            specializations.append(spec)

        for _ in range(random.randint(3, 6)): # 3-6 services per hospital
            serv = service.objects.create(
                service_name=fake.word().capitalize() + " Service",
                hospital=hospital
            )
            services.append(serv)
    print(f"  Created {len(departments)} departments, {len(specializations)} specializations, {len(services)} services.")

    # --- 4. Generate Test_Information ---
    print("Generating Test Information...")
    test_info_list = []
    for _ in range(num_tests):
        test_info = Test_Information.objects.create(
            test_name=fake.word().capitalize() + " Test",
            test_price=str(random.randint(100, 1000))
        )
        test_info_list.append(test_info)
        print(f"  Created Test Info: {test_info.test_name}")

    # --- 5. Generate Doctor_Information ---
    print("Generating Doctors...")
    doctors = []
    doctor_users = User.objects.filter(is_doctor=True)
    for user in doctor_users:
        hospital = get_random_hospital()
        department = random.choice(departments) if departments else None
        specialization_obj = random.choice(specializations) if specializations else None

        if not hospital or not department or not specialization_obj:
            print(f"  Skipping doctor creation for {user.username}: Missing related hospital, department, or specialization.")
            continue

        lat = float(hospital.latitude) + random.uniform(-0.05, 0.05)
        lon = float(hospital.longitude) + random.uniform(-0.05, 0.05)

        doctor = Doctor_Information.objects.create(
            user=user,
            name=fake.name(),
            username=user.username,
            gender=random.choice(['Male', 'Female']),
            description=fake.paragraph(),
            department=random.choice([choice[0] for choice in Doctor_Information.DOCTOR_TYPE]),
            department_name=department,
            specialization=specialization_obj,
            featured_image='doctors/user-default.png',
            certificate_image='doctors_certificate/default.png',
            email=user.email,
            phone_number=fake.phone_number()[:20],
            nid=fake.ssn(),
            visiting_hour=f"{random.randint(9, 17)}:00 - {random.randint(18, 22)}:00",
            consultation_fee=random.randint(500, 2000),
            report_fee=random.randint(200, 800),
            dob=fake.date_of_birth(minimum_age=30, maximum_age=60).strftime('%Y-%m-%d'),
            register_status='Accepted',
            hospital_name=hospital,
            latitude=lat,
            longitude=lon,
            is_marketplace_active=fake.boolean(),
            home_visit_available=fake.boolean(),
            online_consultation_available=fake.boolean(),
            instant_booking_available=fake.boolean(),
            service_radius=random.randint(5, 50),
            home_visit_fee=random.randint(1000, 5000) if fake.boolean() else None,
            online_consultation_fee=random.randint(500, 2000) if fake.boolean() else None,
            average_response_time=random.randint(5, 60),
            marketplace_rating=round(random.uniform(3.0, 5.0), 2),
            total_marketplace_reviews=random.randint(0, 200),
            total_consultations=random.randint(0, 1000)
        )
        doctors.append(doctor)
        print(f"  Created Doctor: {doctor.name}")

    # --- 6. Generate Pharmacists ---
    print("Generating Pharmacists...")
    pharmacists = []
    pharmacist_users = User.objects.filter(is_pharmacist=True)
    for user in pharmacist_users:
        pharmacist = Pharmacist.objects.create(
            user=user,
            name=fake.name(),
            username=user.username,
            degree=fake.word().capitalize() + " in Pharmacy",
            featured_image='pharmacist/user-default.png',
            email=user.email,
            phone_number=random.randint(1000000000, 9999999999),
            age=random.randint(25, 60)
        )
        pharmacists.append(pharmacist)
        print(f"  Created Pharmacist: {pharmacist.name}")

    # --- 7. Generate Clinical_Laboratory_Technicians ---
    print("Generating Lab Workers...")
    lab_workers = []
    labworker_users = User.objects.filter(is_labworker=True)
    for user in labworker_users:
        hospital = get_random_hospital()
        if not hospital:
            print(f"  Skipping lab worker creation for {user.username}: No hospitals available.")
            continue
        lab_worker = Clinical_Laboratory_Technician.objects.create(
            user=user,
            name=fake.name(),
            username=user.username,
            age=random.randint(22, 50),
            email=user.email,
            phone_number=random.randint(1000000000, 9999999999),
            featured_image='technician/user-default.png',
            hospital=hospital
        )
        lab_workers.append(lab_worker)
        print(f"  Created Lab Worker: {lab_worker.name}")

    # --- Generate Admin_Information ---
    print("Generating Admin Information...")
    admin_users = User.objects.filter(is_hospital_admin=True)
    for user in admin_users:
        Admin_Information.objects.create(
            user=user,
            name=fake.name(),
            username=user.username,
            email=user.email,
            phone_number=fake.phone_number()[:20],
            role='hospital'
        )
        print(f"  Created Admin Information for: {user.username}")

    # --- 8. Generate DeliveryPartners ---
    print("Generating Delivery Partners...")
    delivery_partners = []
    delivery_partner_users = User.objects.filter(is_delivery_partner=True)
    for user in delivery_partner_users:
        delivery_partner = DeliveryPartner.objects.create(
            user=user,
            name=fake.name(),
            phone_number=fake.phone_number()[:20],
            vehicle_type=random.choice(['Motorcycle', 'Bicycle', 'Car']),
            license_number=fake.license_plate(),
            current_latitude=fake.latitude(),
            current_longitude=fake.longitude(),
            status=random.choice([choice[0] for choice in DeliveryPartner.PARTNER_STATUS]),
            is_verified=fake.boolean(),
            rating=round(random.uniform(3.0, 5.0), 2),
            total_deliveries=random.randint(0, 1000)
        )
        delivery_partners.append(delivery_partner)
        print(f"  Created Delivery Partner: {delivery_partner.name}")

    # --- 9. Generate Medicines ---
    print("Generating Medicines...")
    medicines = []
    for _ in range(num_medicines):
        medicine = Medicine.objects.create(
            medicine_id=fake.uuid4()[:10],
            name=fake.word().capitalize() + " " + random.choice(["Tablet", "Syrup", "Capsule"]),
            weight=f"{random.randint(10, 500)}mg",
            quantity=random.randint(10, 1000),
            featured_image='medicines/default.png',
            description=fake.paragraph(),
            medicine_type=random.choice([choice[0] for choice in Medicine.MEDICINE_TYPE]),
            medicine_category=random.choice([choice[0] for choice in Medicine.MEDICINE_CATEGORY]),
            price=random.randint(50, 1000),
            stock_quantity=random.randint(0, 500),
            Prescription_reqiuired=random.choice([choice[0] for choice in Medicine.REQUIREMENT_TYPE]),
            is_delivery_available=fake.boolean(),
            delivery_time_minutes=random.randint(30, 120),
            is_emergency_available=fake.boolean(),
            storage_temperature=random.choice(['Room Temp', 'Refrigerated']),
            is_marketplace_active=fake.boolean(),
            supplier_name=fake.company()
        )
        medicines.append(medicine)
        print(f"  Created Medicine: {medicine.name}")

    # --- 10. Generate ServiceProviders (Marketplace) ---
    print("Generating Service Providers (Marketplace)...")
    service_providers = []
    for _ in range(num_hospitals + len(doctors) + len(pharmacists)): # Roughly one per hospital, doctor, pharmacist
        provider_type = random.choice([choice[0] for choice in ServiceProvider.SERVICE_TYPES])
        
        hospital_obj = None
        doctor_obj = None
        pharmacist_obj = None
        name = ""
        
        if provider_type == 'consultation' and doctors:
            doctor_obj = random.choice(doctors)
            name = doctor_obj.name
            lat = doctor_obj.latitude
            lon = doctor_obj.longitude
        elif provider_type == 'medicine_delivery' and pharmacists:
            pharmacist_obj = random.choice(pharmacists)
            name = pharmacist_obj.name
            # Use a random hospital's location for pharmacy service provider if pharmacist doesn't have one
            hospital_for_pharmacy = get_random_hospital()
            lat = hospital_for_pharmacy.latitude if hospital_for_pharmacy else fake.latitude()
            lon = hospital_for_pharmacy.longitude if hospital_for_pharmacy else fake.longitude()
        elif provider_type == 'lab_service' and hospitals:
            hospital_obj = random.choice(hospitals)
            name = hospital_obj.name + " Lab Service"
            lat = hospital_obj.latitude
            lon = hospital_obj.longitude
        elif provider_type == 'home_visit' and doctors:
            doctor_obj = random.choice(doctors)
            name = doctor_obj.name + " Home Visit"
            lat = doctor_obj.latitude
            lon = doctor_obj.longitude
        else:
            # Fallback if no suitable related object found
            name = fake.company() + " Service"
            lat = fake.latitude()
            lon = fake.longitude()

        if not name: # Skip if name is empty due to missing related objects
            continue

        sp = ServiceProvider.objects.create(
            name=name,
            service_type=provider_type,
            hospital=hospital_obj,
            doctor=doctor_obj,
            pharmacist=pharmacist_obj,
            latitude=lat,
            longitude=lon,
            service_radius=random.randint(5, 100),
            availability_status=random.choice([choice[0] for choice in ServiceProvider.AVAILABILITY_STATUS]),
            average_delivery_time=random.randint(15, 180),
            rating=round(random.uniform(3.0, 5.0), 2),
            total_reviews=random.randint(0, 500),
            base_fee=random.randint(50, 500),
            delivery_fee=random.randint(20, 100),
            emergency_fee=random.randint(50, 200)
        )
        service_providers.append(sp)
        print(f"  Created Service Provider: {sp.name} ({sp.service_type})")

    # --- 11. Generate Patients ---
    print("Generating Patients...")
    patients = []
    patient_users = User.objects.filter(is_patient=True)
    for user in patient_users:
        for _ in range(num_patients_per_user):
            patient = Patient.objects.create(
                user=user,
                name=fake.name(),
                username=user.username,
                age=random.randint(18, 80),
                email=user.email,
                phone_number=fake.phone_number()[:20],
                address=fake.address(),
                featured_image='patients/user-default.png',
                blood_group=random.choice(['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']),
                history=fake.sentence(),
                dob=fake.date_of_birth(minimum_age=18, maximum_age=80).strftime('%Y-%m-%d'),
                nid=fake.ssn(),
                serial_number=fake.uuid4()[:10],
                login_status=random.choice(['online', 'offline'])
            )
            patients.append(patient)
            print(f"  Created Patient: {patient.name}")

    # --- 12. Generate Appointments ---
    print("Generating Appointments...")
    appointments = []
    for _ in range(num_appointments_per_patient * len(patients)):
        patient = get_random_patient()
        doctor = get_random_doctor()
        if not patient or not doctor:
            continue
        
        appointment_date = fake.date_between(start_date="-30d", end_date="+30d")
        appointment_time = f"{random.randint(9, 17)}:00"
        
        appointment = Appointment.objects.create(
            date=appointment_date,
            time=appointment_time,
            doctor=doctor,
            patient=patient,
            appointment_type=random.choice([choice[0] for choice in Appointment.APPOINTMENT_TYPE]),
            appointment_status=random.choice([choice[0] for choice in Appointment.APPOINTMENT_STATUS]),
            serial_number=fake.uuid4()[:10],
            payment_status=random.choice(['pending', 'paid']),
            transaction_id=fake.uuid4() if fake.boolean() else None,
            message=fake.sentence() if fake.boolean() else None
        )
        appointments.append(appointment)
        print(f"  Created Appointment for {patient.name} with {doctor.name}")

    # --- 13. Generate Education and Experience for Doctors ---
    print("Generating Doctor Education and Experience...")
    degree_list = [
        "Bachelor of Science in Computer Science",
        "Master of Business Administration",
        "Doctor of Medicine",
        "Juris Doctor",
        "Bachelor of Arts in Psychology",
        "Master of Science in Engineering",
        "Doctor of Philosophy in Biology",
        "Bachelor of Science in Nursing",
        "Master of Public Health",
        "Bachelor of Engineering in Mechanical Engineering",
    ]
    for doctor in doctors:
        for _ in range(random.randint(1, 3)): # 1-3 education entries
            Education.objects.create(
                doctor=doctor,
                degree=random.choice(degree_list),
                institute=fake.company(),
                year_of_completion=str(random.randint(1990, 2015))
            )
        for _ in range(random.randint(1, 3)): # 1-3 experience entries
            Experience.objects.create(
                doctor=doctor,
                work_place_name=fake.company(),
                from_year=str(random.randint(1995, 2010)),
                to_year=str(random.randint(2011, 2023)),
                designation=fake.job()
            )
        print(f"  Added education/experience for Dr. {doctor.name}")

    # --- 14. Generate Reports, Specimens, and Tests ---
    print("Generating Reports, Specimens, and Tests...")
    reports = []
    for _ in range(len(patients) * 2): # Roughly 2 reports per patient
        patient = get_random_patient()
        doctor = get_random_doctor()
        if not patient or not doctor:
            continue
        
        report = Report.objects.create(
            doctor=doctor,
            patient=patient,
            specimen_id=fake.uuid4()[:10],
            specimen_type=random.choice(['Blood', 'Urine', 'Tissue']),
            collection_date=fake.date_this_year().strftime('%Y-%m-%d'),
            receiving_date=fake.date_this_year().strftime('%Y-%m-%d'),
            test_name=fake.word().capitalize() + " Panel",
            result=fake.word(),
            unit=random.choice(['mg/dL', 'g/L', 'cells/mL']),
            referred_value=fake.word(),
            delivery_date=fake.date_this_year().strftime('%Y-%m-%d'),
            other_information=fake.sentence() if fake.boolean() else None
        )
        reports.append(report)

        for _ in range(random.randint(1, 3)): # 1-3 specimens per report
            Specimen.objects.create(
                report=report,
                specimen_type=random.choice(['Blood', 'Urine', 'Tissue']),
                collection_date=fake.date_this_year().strftime('%Y-%m-%d'),
                receiving_date=fake.date_this_year().strftime('%Y-%m-%d')
            )
        
        for _ in range(random.randint(1, 5)): # 1-5 tests per report
            Test.objects.create(
                report=report,
                test_name=fake.word().capitalize() + " Test",
                result=fake.word(),
                unit=random.choice(['mg/dL', 'g/L', 'cells/mL']),
                referred_value=fake.word()
            )
        print(f"  Created Report for {patient.name}")

    # --- 15. Generate Prescriptions, Prescription_medicine, and Prescription_test ---
    print("Generating Prescriptions...")
    prescriptions = []
    for _ in range(num_prescriptions_per_patient * len(patients)):
        patient = get_random_patient()
        doctor = get_random_doctor()
        if not patient or not doctor:
            continue
        
        prescription = Prescription.objects.create(
            doctor=doctor,
            patient=patient,
            create_date=fake.date_this_year().strftime('%Y-%m-%d'),
            medicine_name=fake.word().capitalize(), # This field seems redundant if Prescription_medicine is used
            quantity=str(random.randint(1, 3)),
            days=str(random.randint(5, 30)),
            time=f"{random.randint(8, 20)}:00",
            relation_with_meal=random.choice(['Before Meal', 'After Meal']),
            medicine_description=fake.sentence(),
            test_name=fake.word().capitalize(), # This field seems redundant if Prescription_test is used
            test_description=fake.sentence(),
            extra_information=fake.paragraph() if fake.boolean() else None
        )
        prescriptions.append(prescription)

        for _ in range(random.randint(1, 3)): # 1-3 medicines per prescription
            Prescription_medicine.objects.create(
                prescription=prescription,
                medicine_name=fake.word().capitalize() + " " + random.choice(["Tablet", "Syrup"]),
                quantity=str(random.randint(1, 3)),
                duration=f"{random.randint(5, 30)} days",
                frequency=random.choice(['Once Daily', 'Twice Daily', 'Thrice Daily']),
                relation_with_meal=random.choice(['Before Meal', 'After Meal']),
                instruction=fake.sentence(),
                is_ordered=fake.boolean(),
                order_status=random.choice([choice[0] for choice in Prescription_medicine._meta.get_field('order_status').choices]),
                ordered_date=fake.date_time_this_year() if fake.boolean() else None
            )
        
        for _ in range(random.randint(0, 2)): # 0-2 tests per prescription
            test_info = get_random_test_information()
            if test_info:
                Prescription_test.objects.create(
                    prescription=prescription,
                    test_name=test_info.test_name,
                    test_description=fake.sentence(),
                    test_info_id=test_info.test_id,
                    test_info_price=test_info.test_price,
                    test_info_pay_status=random.choice(['Paid', 'Unpaid'])
                )
        print(f"  Created Prescription for {patient.name}")

    # --- 16. Generate Cart and Order (Pharmacy) ---
    print("Generating Pharmacy Carts and Orders...")
    pharmacy_orders = []
    for patient in patients:
        if random.random() < 0.5: # 50% chance to create an order
            cart_items = []
            for _ in range(random.randint(1, 3)): # 1-3 items per cart
                medicine = get_random_medicine()
                if medicine:
                    cart_item = Cart.objects.create(
                        user=patient.user,
                        item=medicine,
                        quantity=random.randint(1, 5),
                        purchased=True # Assume purchased for order
                    )
                    cart_items.append(cart_item)
            
            if cart_items:
                order = Order.objects.create(
                    user=patient.user,
                    ordered=True,
                    created=fake.date_time_this_year(),
                    payment_status=random.choice(['paid', 'pending']),
                    trans_ID=fake.uuid4()
                )
                order.orderitems.set(cart_items)
                pharmacy_orders.append(order)
                print(f"  Created Pharmacy Order for {patient.name}")

    # --- 17. Generate testCart and testOrder (Doctor Tests) ---
    print("Generating Doctor Test Carts and Orders...")
    doctor_test_orders = []
    for patient in patients:
        if random.random() < 0.5: # 50% chance to create a test order
            test_cart_items = []
            for _ in range(random.randint(1, 2)): # 1-2 tests per order
                prescription_test = Prescription_test.objects.order_by('?').first() # Get a random prescription test
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
                    created=fake.date_time_this_year(),
                    payment_status=random.choice(['paid', 'pending']),
                    trans_ID=fake.uuid4()
                )
                test_order.orderitems.set(test_cart_items)
                doctor_test_orders.append(test_order)
                print(f"  Created Doctor Test Order for {patient.name}")

    # --- 18. Generate Payments ---
    print("Generating Payments...")
    for _ in range(num_users * 2): # Generate a few payments
        patient = get_random_patient()
        if not patient:
            continue
        
        payment_type = random.choice(['appointment', 'medicine', 'lab_test'])
        
        appointment_obj = None
        order_obj = None
        test_order_obj = None
        prescription_obj = None

        if payment_type == 'appointment':
            appointment_obj = Appointment.objects.filter(patient=patient).order_by('?').first()
            if not appointment_obj: continue
        elif payment_type == 'medicine':
            order_obj = Order.objects.filter(user=patient.user).order_by('?').first()
            if not order_obj: continue
        elif payment_type == 'lab_test':
            test_order_obj = testOrder.objects.filter(user=patient.user).order_by('?').first()
            if not test_order_obj: continue
        
        # Link to a random prescription if available
        prescription_obj = Prescription.objects.filter(patient=patient).order_by('?').first()

        Payment.objects.create(
            invoice_number=fake.uuid4()[:10],
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
            country=fake.country(),
            transaction_id=fake.uuid4(),
            val_transaction_id=fake.uuid4(),
            currency_amount=str(random.randint(100, 5000)),
            consulation_fee=str(random.randint(50, 1000)) if random.random() < 0.5 else None,
            report_fee=str(random.randint(50, 500)) if random.random() < 0.5 else None,
            card_type=random.choice(['VISA', 'MasterCard']) if fake.boolean() else None,
            card_no=fake.credit_card_number() if fake.boolean() else None,
            bank_transaction_id=fake.uuid4() if fake.boolean() else None,
            status=random.choice(['VALID', 'FAILED', 'PENDING']),
            transaction_date=fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S'),
            currency='BDT',
            card_issuer=fake.company() if fake.boolean() else None,
            card_brand=fake.credit_card_provider() if fake.boolean() else None
        )
        print(f"  Created Payment for {patient.name} ({payment_type})")

    # --- 19. Generate Marketplace Orders ---
    print("Generating Marketplace Orders...")
    for _ in range(num_marketplace_orders):
        user = get_random_user()
        service_provider = get_random_service_provider()
        delivery_partner = get_random_delivery_partner()
        
        if not user or not service_provider:
            continue

        order_type = service_provider.service_type # Match order type to service provider type
        
        MarketplaceOrder.objects.create(
            user=user,
            service_provider=service_provider,
            delivery_partner=delivery_partner if delivery_partner and fake.boolean() else None,
            order_type=order_type,
            status=random.choice([choice[0] for choice in MarketplaceOrder.ORDER_STATUS]),
            priority=random.choice([choice[0] for choice in MarketplaceOrder.PRIORITY]),
            delivery_latitude=fake.latitude(),
            delivery_longitude=fake.longitude(),
            delivery_address=fake.address(),
            subtotal=random.randint(100, 2000),
            delivery_fee=random.randint(20, 100),
            total_amount=random.randint(150, 2100),
            estimated_delivery_time=fake.date_time_between(start_date="now", end_date="+2h"),
            actual_delivery_time=fake.date_time_between(start_date="-1h", end_date="now") if fake.boolean() else None,
            payment_status=random.choice(['paid', 'pending', 'failed']),
            transaction_id=fake.uuid4() if fake.boolean() else None
        )
        print(f"  Created Marketplace Order for {user.username} ({order_type})")

    # --- 20. Generate Chat Messages ---
    print("Generating Chat Messages...")
    users_for_chat = list(User.objects.all())
    if len(users_for_chat) >= 2:
        for _ in range(num_chat_messages):
            user1 = random.choice(users_for_chat)
            user2 = random.choice(users_for_chat)
            while user1 == user2: # Ensure different users
                user2 = random.choice(users_for_chat)
            
            chatMessages.objects.create(
                user_from=user1,
                user_to=user2,
                message=fake.sentence(),
                date_created=fake.date_time_this_year()
            )
            print(f"  Created Chat Message between {user1.username} and {user2.username}")

    # --- 21. Generate Doctor Reviews ---
    print("Generating Doctor Reviews...")
    for _ in range(num_doctor_reviews):
        doctor = get_random_doctor()
        patient = get_random_patient()
        if not doctor or not patient:
            continue
        
        Doctor_review.objects.create(
            doctor=doctor,
            patient=patient,
            title=fake.sentence(nb_words=3),
            message=fake.paragraph()
        )
        print(f"  Created Doctor Review for {doctor.name} by {patient.name}")

    print("Comprehensive fake data generation complete!")

if __name__ == '__main__':
    # This part is for direct execution if needed, but running via shell is preferred.
    # from django.core.management import setup_environ
    # from healthstack import settings
    # setup_environ(settings)
    generate_all_fake_data()
