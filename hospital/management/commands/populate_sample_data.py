
from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth.hashers import make_password
from hospital.models import User, Patient, Hospital_Information
from doctor.models import Doctor_Information, Prescription, Prescription_medicine, Prescription_test, Appointment
from pharmacy.models import Pharmacist, Medicine, Cart, Order
from hospital_admin.models import Admin_Information, hospital_department, specialization, service, Clinical_Laboratory_Technician, test_information
import random
from datetime import datetime, timedelta
import uuid

class Command(BaseCommand):
    help = 'Populate database with sample data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating sample data...'))
        
        with transaction.atomic():
            # Create Hospitals
            hospitals = self.create_hospitals()
            
            # Create Departments and Specializations
            departments = self.create_departments()
            specializations = self.create_specializations()
            
            # Create Test Information
            tests = self.create_test_information()
            
            # Create Admin Users
            admins = self.create_admin_users(hospitals)
            
            # Create Doctor Users
            doctors = self.create_doctor_users(hospitals, departments, specializations)
            
            # Create Patient Users
            patients = self.create_patient_users()
            
            # Create Pharmacist Users
            pharmacists = self.create_pharmacist_users()
            
            # Create Medicines
            medicines = self.create_medicines()
            
            # Create Lab Workers
            lab_workers = self.create_lab_workers(hospitals)
            
            # Create Appointments
            appointments = self.create_appointments(doctors, patients)
            
            # Create Prescriptions
            prescriptions = self.create_prescriptions(doctors, patients)
            
            # Create Cart Items
            self.create_cart_items(patients, medicines)
            
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created sample data:\n'
                f'- {len(hospitals)} hospitals\n'
                f'- {len(departments)} departments\n'
                f'- {len(specializations)} specializations\n'
                f'- {len(tests)} test types\n'
                f'- {len(admins)} admin users\n'
                f'- {len(doctors)} doctors\n'
                f'- {len(patients)} patients\n'
                f'- {len(pharmacists)} pharmacists\n'
                f'- {len(medicines)} medicines\n'
                f'- {len(lab_workers)} lab workers\n'
                f'- {len(appointments)} appointments\n'
                f'- {len(prescriptions)} prescriptions'
            )
        )

    def create_hospitals(self):
        hospitals_data = [
            {'name': 'City General Hospital', 'address': '123 Main St, Downtown', 'type': 'public'},
            {'name': 'St. Mary Medical Center', 'address': '456 Oak Ave, Midtown', 'type': 'private'},
            {'name': 'Metropolitan Hospital', 'address': '789 Pine Rd, Uptown', 'type': 'private'},
            {'name': 'Community Health Center', 'address': '321 Elm St, Southside', 'type': 'public'},
            {'name': 'Regional Medical Complex', 'address': '654 Maple Dr, Eastside', 'type': 'private'},
            {'name': 'University Hospital', 'address': '987 College Blvd, Campus', 'type': 'public'},
            {'name': 'Children\'s Hospital', 'address': '147 Kids Lane, Family District', 'type': 'private'},
            {'name': 'Heart & Vascular Institute', 'address': '258 Cardiac Way, Medical Plaza', 'type': 'private'},
        ]
        
        hospitals = []
        for data in hospitals_data:
            hospital = Hospital_Information.objects.create(
                name=data['name'],
                address=data['address'],
                hospital_type=data['type'],
                description=f"Leading healthcare provider in the region offering comprehensive medical services.",
                email=f"info@{data['name'].lower().replace(' ', '').replace('\'', '')}.com",
                phone_number=random.randint(1000000000, 9999999999),
                general_bed_no=random.randint(50, 200),
                available_icu_no=random.randint(10, 30),
                regular_cabin_no=random.randint(20, 50),
                emergency_cabin_no=random.randint(5, 15),
                vip_cabin_no=random.randint(5, 20),
                latitude=round(random.uniform(23.7, 23.9), 6),
                longitude=round(random.uniform(90.3, 90.5), 6)
            )
            hospitals.append(hospital)
        
        return hospitals

    def create_departments(self):
        dept_names = [
            'Cardiology', 'Neurology', 'Pediatrics', 'Orthopedics', 'Dermatology',
            'Gastroenterology', 'Psychiatry', 'Radiology', 'Emergency Medicine',
            'Internal Medicine', 'Surgery', 'Oncology', 'Urology', 'ENT',
            'Gynecology', 'Anesthesiology', 'Pathology', 'Ophthalmology'
        ]
        
        departments = []
        for name in dept_names:
            dept = hospital_department.objects.create(
                department_name=name,
                department_description=f"Department specializing in {name.lower()} care and treatment."
            )
            departments.append(dept)
        
        return departments

    def create_specializations(self):
        spec_names = [
            'Interventional Cardiology', 'Pediatric Neurology', 'Orthopedic Surgery',
            'Cosmetic Dermatology', 'Gastroenterology', 'Child Psychiatry',
            'Emergency Medicine', 'General Surgery', 'Medical Oncology',
            'Urological Surgery', 'Head and Neck Surgery', 'Obstetrics',
            'Cardiac Anesthesia', 'Clinical Pathology', 'Retinal Surgery'
        ]
        
        specializations = []
        for name in spec_names:
            spec = specialization.objects.create(
                specialization_name=name,
                specialization_description=f"Specialized expertise in {name.lower()}."
            )
            specializations.append(spec)
        
        return specializations

    def create_test_information(self):
        tests_data = [
            {'name': 'Complete Blood Count', 'price': 800},
            {'name': 'Lipid Profile', 'price': 1200},
            {'name': 'Liver Function Test', 'price': 1500},
            {'name': 'Kidney Function Test', 'price': 1300},
            {'name': 'Thyroid Function Test', 'price': 1800},
            {'name': 'Blood Sugar (Fasting)', 'price': 300},
            {'name': 'HbA1c', 'price': 600},
            {'name': 'Chest X-Ray', 'price': 800},
            {'name': 'ECG', 'price': 500},
            {'name': 'Echocardiogram', 'price': 2500},
            {'name': 'CT Scan Head', 'price': 5000},
            {'name': 'MRI Brain', 'price': 8000},
            {'name': 'Ultrasound Abdomen', 'price': 1500},
            {'name': 'Urine Analysis', 'price': 200},
            {'name': 'Stool Analysis', 'price': 300}
        ]
        
        tests = []
        for data in tests_data:
            test = test_information.objects.create(
                test_name=data['name'],
                test_price=data['price'],
                test_description=f"Medical test for {data['name'].lower()} analysis."
            )
            tests.append(test)
        
        return tests

    def create_admin_users(self, hospitals):
        admins = []
        for i, hospital in enumerate(hospitals[:5]):  # Create 5 admin users
            user = User.objects.create(
                username=f'admin{i+1}',
                email=f'admin{i+1}@hospital.com',
                password=make_password('admin123'),
                first_name=f'Admin',
                last_name=f'User {i+1}',
                is_hospital_admin=True
            )
            
            admin = Admin_Information.objects.create(
                user=user,
                username=user.username,
                email=user.email,
                name=f'Admin User {i+1}',
                hospital=hospital
            )
            admins.append(admin)
        
        return admins

    def create_doctor_users(self, hospitals, departments, specializations):
        doctor_names = [
            ('Dr. Sarah', 'Johnson'), ('Dr. Michael', 'Chen'), ('Dr. Emily', 'Rodriguez'),
            ('Dr. David', 'Thompson'), ('Dr. Lisa', 'Anderson'), ('Dr. James', 'Wilson'),
            ('Dr. Maria', 'Garcia'), ('Dr. Robert', 'Taylor'), ('Dr. Jennifer', 'Brown'),
            ('Dr. Christopher', 'Davis'), ('Dr. Amanda', 'Miller'), ('Dr. Daniel', 'Moore'),
            ('Dr. Jessica', 'Jackson'), ('Dr. Matthew', 'Martin'), ('Dr. Ashley', 'Lee'),
            ('Dr. Joshua', 'Perez'), ('Dr. Stephanie', 'White'), ('Dr. Andrew', 'Harris'),
            ('Dr. Michelle', 'Clark'), ('Dr. Kevin', 'Lewis'), ('Dr. Rachel', 'Walker'),
            ('Dr. Brian', 'Hall'), ('Dr. Nicole', 'Allen'), ('Dr. Ryan', 'Young'),
            ('Dr. Samantha', 'King')
        ]
        
        doctors = []
        for i, (first_name, last_name) in enumerate(doctor_names):
            username = f'doctor{i+1}'
            user = User.objects.create(
                username=username,
                email=f'{username}@hospital.com',
                password=make_password('doctor123'),
                first_name=first_name,
                last_name=last_name,
                is_doctor=True
            )
            
            doctor = Doctor_Information.objects.create(
                user=user,
                username=user.username,
                email=user.email,
                name=f'{first_name} {last_name}',
                gender=random.choice(['Male', 'Female']),
                description=f'Experienced physician with expertise in patient care.',
                department=random.choice(['Cardiologists', 'Neurologists', 'Pediatricians', 'Physiatrists', 'Dermatologists']),
                department_name=random.choice(departments),
                specialization=random.choice(specializations),
                phone_number=f'01{random.randint(700000000, 999999999)}',
                nid=f'{random.randint(1000000000000, 9999999999999)}',
                visiting_hour=random.choice(['9:00 AM - 5:00 PM', '2:00 PM - 8:00 PM', '10:00 AM - 6:00 PM']),
                consultation_fee=random.randint(800, 2000),
                report_fee=random.randint(500, 1000),
                dob=f'{random.randint(1970, 1990)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}',
                latitude=round(random.uniform(23.7, 23.9), 6),
                longitude=round(random.uniform(90.3, 90.5), 6),
                is_marketplace_active=random.choice([True, False]),
                home_visit_available=random.choice([True, False]),
                online_consultation_available=True,
                instant_booking_available=random.choice([True, False]),
                service_radius=random.randint(5, 25),
                home_visit_fee=random.randint(1500, 3000),
                online_consultation_fee=random.randint(600, 1500),
                average_response_time=random.randint(15, 60),
                marketplace_rating=round(random.uniform(4.0, 5.0), 1),
                total_marketplace_reviews=random.randint(10, 100),
                total_consultations=random.randint(50, 500),
                institute=random.choice(['Dhaka Medical College', 'Chittagong Medical College', 'Sylhet MAG Osmani Medical College']),
                degree=random.choice(['MBBS', 'MBBS, MD', 'MBBS, FCPS']),
                completion_year=str(random.randint(2000, 2015)),
                work_place=random.choice(hospitals).name,
                designation=random.choice(['Consultant', 'Assistant Professor', 'Associate Professor', 'Professor']),
                start_year=str(random.randint(2010, 2020)),
                end_year=str(random.randint(2021, 2024)),
                register_status='approved',
                hospital_name=random.choice(hospitals)
            )
            doctors.append(doctor)
        
        return doctors

    def create_patient_users(self):
        patient_names = [
            ('John', 'Smith'), ('Emma', 'Johnson'), ('Michael', 'Williams'), ('Olivia', 'Brown'),
            ('William', 'Jones'), ('Ava', 'Garcia'), ('James', 'Miller'), ('Isabella', 'Davis'),
            ('Benjamin', 'Rodriguez'), ('Sophia', 'Martinez'), ('Lucas', 'Hernandez'), ('Charlotte', 'Lopez'),
            ('Henry', 'Gonzalez'), ('Amelia', 'Wilson'), ('Alexander', 'Anderson'), ('Mia', 'Thomas'),
            ('Sebastian', 'Taylor'), ('Harper', 'Moore'), ('Jack', 'Jackson'), ('Evelyn', 'Martin'),
            ('Owen', 'Lee'), ('Abigail', 'Perez'), ('Theodore', 'Thompson'), ('Emily', 'White'),
            ('Luke', 'Harris'), ('Elizabeth', 'Sanchez'), ('Mason', 'Clark'), ('Sofia', 'Ramirez'),
            ('Levi', 'Lewis'), ('Avery', 'Robinson')
        ]
        
        patients = []
        for i, (first_name, last_name) in enumerate(patient_names):
            username = f'patient{i+1}'
            user = User.objects.create(
                username=username,
                email=f'{username}@email.com',
                password=make_password('patient123'),
                first_name=first_name,
                last_name=last_name,
                is_patient=True
            )
            
            patient = Patient.objects.create(
                user=user,
                username=user.username,
                email=user.email,
                name=f'{first_name} {last_name}',
                age=random.randint(18, 80),
                phone_number=random.randint(1700000000, 1999999999),
                address=f'{random.randint(1, 999)} {random.choice(["Main St", "Oak Ave", "Pine Rd", "Elm St", "Maple Dr"])}',
                blood_group=random.choice(['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']),
                history=random.choice(['No significant history', 'Hypertension', 'Diabetes', 'Asthma', 'Allergies']),
                dob=f'{random.randint(1940, 2005)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}',
                nid=f'{random.randint(1000000000000, 9999999999999)}',
                serial_number=f'P{random.randint(10000, 99999)}',
                login_status='offline'
            )
            patients.append(patient)
        
        return patients

    def create_pharmacist_users(self):
        pharmacist_names = [
            ('Ahmed', 'Rahman'), ('Fatima', 'Khan'), ('Mohammad', 'Islam'), ('Rashida', 'Begum'),
            ('Karim', 'Uddin'), ('Nasreen', 'Akter'), ('Rafiq', 'Ahmed'), ('Salma', 'Khatun'),
            ('Mizanur', 'Rahman'), ('Ruma', 'Begum')
        ]
        
        pharmacists = []
        for i, (first_name, last_name) in enumerate(pharmacist_names):
            username = f'pharmacist{i+1}'
            user = User.objects.create(
                username=username,
                email=f'{username}@pharmacy.com',
                password=make_password('pharmacist123'),
                first_name=first_name,
                last_name=last_name,
                is_pharmacist=True
            )
            
            pharmacist = Pharmacist.objects.create(
                user=user,
                username=user.username,
                email=user.email,
                name=f'{first_name} {last_name}',
                degree=random.choice(['B.Pharm', 'PharmD', 'M.Pharm']),
                phone_number=random.randint(1700000000, 1999999999),
                age=random.randint(25, 55)
            )
            pharmacists.append(pharmacist)
        
        return pharmacists

    def create_medicines(self):
        medicines_data = [
            {'name': 'Paracetamol', 'type': 'tablets', 'category': 'fever'},
            {'name': 'Ibuprofen', 'type': 'tablets', 'category': 'pain'},
            {'name': 'Cough Syrup', 'type': 'syrup', 'category': 'cough'},
            {'name': 'Cetirizine', 'type': 'tablets', 'category': 'allergy'},
            {'name': 'Metformin', 'type': 'tablets', 'category': 'diabetes'},
            {'name': 'Lisinopril', 'type': 'tablets', 'category': 'bloodpressure'},
            {'name': 'Salbutamol Inhaler', 'type': 'general', 'category': 'asthma'},
            {'name': 'Vitamin D3', 'type': 'capsule', 'category': 'vitamins'},
            {'name': 'Omeprazole', 'type': 'capsule', 'category': 'digestivehealth'},
            {'name': 'Antibiotic Cream', 'type': 'general', 'category': 'skin'},
            {'name': 'Amoxicillin', 'type': 'capsule', 'category': 'infection'},
            {'name': 'Eye Drops', 'type': 'general', 'category': 'eye'},
            {'name': 'Ear Drops', 'type': 'general', 'category': 'ear'},
            {'name': 'Cold Medicine', 'type': 'tablets', 'category': 'cold'},
            {'name': 'Flu Vaccine', 'type': 'general', 'category': 'flu'},
            {'name': 'Heart Medication', 'type': 'tablets', 'category': 'heartdisease'},
            {'name': 'Neurology Pills', 'type': 'tablets', 'category': 'nurological'},
            {'name': 'Aspirin', 'type': 'tablets', 'category': 'pain'},
            {'name': 'Antacid', 'type': 'tablets', 'category': 'digestivehealth'},
            {'name': 'Multivitamin', 'type': 'tablets', 'category': 'vitamins'},
            {'name': 'Calcium Supplement', 'type': 'tablets', 'category': 'vitamins'},
            {'name': 'Iron Tablets', 'type': 'tablets', 'category': 'vitamins'},
            {'name': 'Probiotics', 'type': 'capsule', 'category': 'digestivehealth'},
            {'name': 'Pain Relief Gel', 'type': 'general', 'category': 'pain'},
            {'name': 'Antiseptic Solution', 'type': 'general', 'category': 'skin'}
        ]
        
        medicines = []
        for data in medicines_data:
            medicine = Medicine.objects.create(
                medicine_id=f'MED{random.randint(1000, 9999)}',
                name=data['name'],
                weight=f'{random.randint(50, 500)}mg',
                quantity=random.randint(10, 100),
                description=f'Effective {data["name"].lower()} for medical treatment.',
                medicine_type=data['type'],
                medicine_category=data['category'],
                price=random.randint(50, 500),
                stock_quantity=random.randint(50, 200),
                Prescription_reqiuired=random.choice(['yes', 'no']),
                is_delivery_available=True,
                delivery_time_minutes=random.randint(30, 120),
                is_emergency_available=random.choice([True, False]),
                storage_temperature=random.choice(['Room Temperature', 'Refrigerated', 'Controlled']),
                is_marketplace_active=True,
                supplier_name=f'Supplier {random.randint(1, 10)}'
            )
            medicines.append(medicine)
        
        return medicines

    def create_lab_workers(self, hospitals):
        lab_worker_names = [
            ('Shahin', 'Alam'), ('Farhana', 'Islam'), ('Kamal', 'Hossain'), ('Rashida', 'Khatun'),
            ('Mizanur', 'Rahman'), ('Nasreen', 'Begum'), ('Rafiqul', 'Islam'), ('Salma', 'Akter')
        ]
        
        lab_workers = []
        for i, (first_name, last_name) in enumerate(lab_worker_names):
            username = f'labworker{i+1}'
            user = User.objects.create(
                username=username,
                email=f'{username}@lab.com',
                password=make_password('lab123'),
                first_name=first_name,
                last_name=last_name,
                is_labworker=True
            )
            
            lab_worker = Clinical_Laboratory_Technician.objects.create(
                user=user,
                username=user.username,
                email=user.email,
                name=f'{first_name} {last_name}',
                hospital=random.choice(hospitals)
            )
            lab_workers.append(lab_worker)
        
        return lab_workers

    def create_appointments(self, doctors, patients):
        appointments = []
        for i in range(50):  # Create 50 appointments
            date = datetime.now().date() + timedelta(days=random.randint(-30, 30))
            time = f'{random.randint(9, 17)}:{random.choice(["00", "30"])}'
            
            appointment = Appointment.objects.create(
                date=date,
                time=time,
                doctor=random.choice(doctors),
                patient=random.choice(patients),
                appointment_type=random.choice(['report', 'checkup']),
                appointment_status=random.choice(['pending', 'confirmed', 'cancelled']),
                serial_number=f'A{random.randint(1000, 9999)}',
                payment_status=random.choice(['pending', 'paid', 'failed']),
                transaction_id=f'TXN{random.randint(100000, 999999)}',
                message=random.choice(['Regular checkup', 'Follow-up visit', 'Emergency consultation', 'Routine examination'])
            )
            appointments.append(appointment)
        
        return appointments

    def create_prescriptions(self, doctors, patients):
        medicine_names = [
            'Paracetamol 500mg', 'Ibuprofen 400mg', 'Amoxicillin 250mg', 'Cetirizine 10mg',
            'Omeprazole 20mg', 'Metformin 500mg', 'Lisinopril 10mg', 'Atorvastatin 20mg',
            'Levothyroxine 50mcg', 'Salbutamol 100mcg', 'Prednisolone 5mg', 'Diclofenac 50mg'
        ]
        
        prescriptions = []
        for i in range(40):  # Create 40 prescriptions
            prescription = Prescription.objects.create(
                doctor=random.choice(doctors),
                patient=random.choice(patients),
                create_date=datetime.now().strftime('%Y-%m-%d'),
                medicine_name=random.choice(medicine_names),
                quantity=f'{random.randint(10, 30)} tablets',
                days=f'{random.randint(7, 30)} days',
                time=random.choice(['Morning', 'Afternoon', 'Evening', '3 times daily']),
                relation_with_meal=random.choice(['Before meal', 'After meal', 'With meal']),
                medicine_description='Take as prescribed by doctor',
                test_name=random.choice(['Blood Test', 'Urine Test', 'X-Ray', 'CT Scan', 'None']),
                test_description='Follow up test as recommended',
                extra_information='Complete the full course of medication'
            )
            prescriptions.append(prescription)
            
            # Create prescription medicines
            for j in range(random.randint(1, 4)):
                Prescription_medicine.objects.create(
                    prescription=prescription,
                    medicine_name=random.choice(medicine_names),
                    quantity=f'{random.randint(10, 30)}',
                    duration=f'{random.randint(7, 30)} days',
                    frequency=random.choice(['Once daily', 'Twice daily', '3 times daily']),
                    relation_with_meal=random.choice(['Before meal', 'After meal', 'With meal']),
                    instruction='Take as directed',
                    is_ordered=random.choice([True, False]),
                    order_status=random.choice(['pending', 'ordered', 'delivered', 'cancelled'])
                )
        
        return prescriptions

    def create_cart_items(self, patients, medicines):
        # Create some cart items for patients
        for i in range(20):
            patient = random.choice(patients)
            medicine = random.choice(medicines)
            
            # Check if cart item already exists
            if not Cart.objects.filter(user=patient.user, item=medicine, purchased=False).exists():
                Cart.objects.create(
                    user=patient.user,
                    item=medicine,
                    quantity=random.randint(1, 5),
                    purchased=False
                )
