
from django.db import models
from django.conf import settings
from hospital.models import Hospital_Information, User
# Use string references to avoid circular imports
# from doctor.models import Doctor_Information
# from pharmacy.models import Pharmacist

class ServiceProvider(models.Model):
    SERVICE_TYPES = (
        ('consultation', 'Medical Consultation'),
        ('medicine_delivery', 'Medicine Delivery'),
        ('lab_service', 'Lab Service'),
        ('home_visit', 'Home Visit'),
    )
    
    AVAILABILITY_STATUS = (
        ('available', 'Available'),
        ('busy', 'Busy'),
        ('offline', 'Offline'),
    )
    
    provider_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPES)
    hospital = models.ForeignKey(Hospital_Information, on_delete=models.CASCADE, null=True, blank=True)
    doctor = models.ForeignKey('doctor.Doctor_Information', on_delete=models.CASCADE, null=True, blank=True)
    pharmacist = models.ForeignKey('pharmacy.Pharmacist', on_delete=models.CASCADE, null=True, blank=True)
    
    # Location and delivery
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    service_radius = models.IntegerField(default=10)  # in kilometers
    
    # Availability
    availability_status = models.CharField(max_length=20, choices=AVAILABILITY_STATUS, default='available')
    average_delivery_time = models.IntegerField(default=60)  # in minutes
    
    # Ratings
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.0)
    total_reviews = models.IntegerField(default=0)
    
    # Fees
    base_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=40)
    emergency_fee = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.service_type}"

class DeliveryPartner(models.Model):
    PARTNER_STATUS = (
        ('available', 'Available'),
        ('busy', 'Busy'),
        ('offline', 'Offline'),
    )
    
    partner_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    vehicle_type = models.CharField(max_length=50)
    license_number = models.CharField(max_length=100)
    
    # Location
    current_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    current_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=PARTNER_STATUS, default='offline')
    is_verified = models.BooleanField(default=False)
    
    # Ratings
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.0)
    total_deliveries = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.vehicle_type}"

class MarketplaceOrder(models.Model):
    ORDER_STATUS = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('preparing', 'Preparing'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    
    ORDER_TYPE = (
        ('consultation', 'Consultation'),
        ('medicine', 'Medicine'),
        ('lab_test', 'Lab Test'),
        ('home_visit', 'Home Visit'),
    )
    
    PRIORITY = (
        ('normal', 'Normal'),
        ('urgent', 'Urgent'),
        ('emergency', 'Emergency'),
    )
    
    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service_provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    delivery_partner = models.ForeignKey(DeliveryPartner, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Order details
    order_type = models.CharField(max_length=20, choices=ORDER_TYPE)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')
    priority = models.CharField(max_length=20, choices=PRIORITY, default='normal')
    
    # Location
    delivery_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    delivery_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    delivery_address = models.TextField()
    
    # Pricing
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Timing
    estimated_delivery_time = models.DateTimeField()
    actual_delivery_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Payment
    payment_status = models.CharField(max_length=20, default='pending')
    transaction_id = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return f"Order #{self.order_id} - {self.order_type}"
