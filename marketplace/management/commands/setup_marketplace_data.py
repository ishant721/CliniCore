
from django.core.management.base import BaseCommand
from django.db import transaction
from marketplace.models import ServiceProvider
from doctor.models import Doctor_Information
from pharmacy.models import Pharmacist
from hospital.models import Hospital_Information
import random

class Command(BaseCommand):
    help = 'Setup initial marketplace data by creating service providers from existing doctors and pharmacists'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Setting up marketplace data...'))
        
        with transaction.atomic():
            # Create service providers for doctors who are marketplace active
            doctors = Doctor_Information.objects.filter(is_marketplace_active=True)
            created_doctor_providers = 0
            
            for doctor in doctors:
                # Check if service provider already exists
                if not ServiceProvider.objects.filter(doctor=doctor).exists():
                    provider = ServiceProvider.objects.create(
                        name=f"Dr. {doctor.name}",
                        service_type='consultation',
                        doctor=doctor,
                        hospital=doctor.hospital_name,
                        latitude=doctor.latitude,
                        longitude=doctor.longitude,
                        service_radius=doctor.service_radius or 10,
                        availability_status='available',
                        average_delivery_time=doctor.average_response_time or 30,
                        rating=doctor.marketplace_rating or 5.0,
                        total_reviews=doctor.total_marketplace_reviews or 0,
                        base_fee=doctor.online_consultation_fee or doctor.consultation_fee or 500,
                        delivery_fee=50,
                        emergency_fee=200
                    )
                    created_doctor_providers += 1
                    self.stdout.write(f'Created service provider for Dr. {doctor.name}')
            
            # Create service providers for pharmacists
            pharmacists = Pharmacist.objects.all()
            created_pharmacy_providers = 0
            
            for pharmacist in pharmacists:
                # Check if service provider already exists
                if not ServiceProvider.objects.filter(pharmacist=pharmacist).exists():
                    provider = ServiceProvider.objects.create(
                        name=f"{pharmacist.name} Pharmacy",
                        service_type='medicine_delivery',
                        pharmacist=pharmacist,
                        availability_status='available',
                        average_delivery_time=random.randint(30, 90),
                        rating=round(random.uniform(4.0, 5.0), 1),
                        total_reviews=random.randint(10, 100),
                        base_fee=0,  # No base fee for medicine delivery
                        delivery_fee=random.choice([40, 50, 60]),
                        emergency_fee=100
                    )
                    created_pharmacy_providers += 1
                    self.stdout.write(f'Created service provider for {pharmacist.name} Pharmacy')
            
            # Update existing providers with missing data
            providers = ServiceProvider.objects.all()
            updated_providers = 0
            
            for provider in providers:
                updated = False
                
                if not provider.rating or provider.rating == 0:
                    provider.rating = round(random.uniform(4.0, 5.0), 1)
                    updated = True
                
                if not provider.total_reviews:
                    provider.total_reviews = random.randint(5, 50)
                    updated = True
                
                if provider.service_type == 'consultation' and provider.doctor:
                    if not provider.base_fee or provider.base_fee == 0:
                        provider.base_fee = provider.doctor.online_consultation_fee or provider.doctor.consultation_fee or 500
                        updated = True
                
                if updated:
                    provider.save()
                    updated_providers += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully setup marketplace data:\n'
                f'- Created {created_doctor_providers} doctor service providers\n'
                f'- Created {created_pharmacy_providers} pharmacy service providers\n'
                f'- Updated {updated_providers} existing providers'
            )
        )
