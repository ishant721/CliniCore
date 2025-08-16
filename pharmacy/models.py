from django.db import models
from django.conf import settings
import uuid
from doctor.models import Prescription

from hospital.models import User, Patient


# Create your models here.

class Pharmacist(models.Model):
    pharmacist_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='pharmacist')
    name = models.CharField(max_length=200, null=True, blank=True)
    username = models.CharField(max_length=200, null=True, blank=True)
    degree = models.CharField(max_length=200, null=True, blank=True)
    featured_image = models.ImageField(upload_to='doctors/', default='pharmacist/user-default.png', null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.user.username)


class PharmacyShop(models.Model):
    shop_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=300)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(max_length=200, null=True, blank=True)
    license_number = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    delivery_available = models.BooleanField(default=True)
    delivery_radius = models.IntegerField(default=10)  # in kilometers
    average_delivery_time = models.IntegerField(default=60)  # in minutes
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.0)
    total_reviews = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Medicine(models.Model):
    MEDICINE_TYPE = (
        ('tablets', 'tablets'),
        ('syrup', 'syrup'),
        ('capsule', 'capsule'),
        ('general', 'general'),
    )
    REQUIREMENT_TYPE = (
        ('yes', 'yes'),
        ('no', 'no'),
    )
    
    MEDICINE_CATEGORY = (
        ('fever', 'fever'),
        ('pain', 'pain'),
        ('cough', 'cough'),
        ('cold', 'cold'),
        ('flu', 'flu'),
        ('diabetes', 'diabetes'),
        ('eye', 'eye'),
        ('ear', 'ear'),
        ('allergy', 'allergy'),
        ('asthma', 'asthma'),
        ('bloodpressure', 'bloodpressure'),
        ('heartdisease', 'heartdisease'),
        ('vitamins', 'vitamins'),
        ('digestivehealth', 'digestivehealth'),
        ('skin', 'skin'),
        ('infection', 'infection'),
        ('nurological', 'nurological'),
    )
    
    serial_number = models.AutoField(primary_key=True)
    medicine_id = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    generic_name = models.CharField(max_length=200, null=True, blank=True)
    manufacturer = models.CharField(max_length=200, null=True, blank=True)
    weight = models.CharField(max_length=200, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True, default=0)
    featured_image = models.ImageField(upload_to='medicines/', default='medicines/default.png', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    medicine_type = models.CharField(max_length=200, choices=MEDICINE_TYPE, null=True, blank=True)
    medicine_category = models.CharField(max_length=200, choices=MEDICINE_CATEGORY, null=True, blank=True)
    price = models.IntegerField(null=True, blank=True, default=0)
    stock_quantity = models.IntegerField(null=True, blank=True, default=0)
    Prescription_reqiuired = models.CharField(max_length=200, choices=REQUIREMENT_TYPE, null=True, blank=True)
    pharmacy_shop = models.ForeignKey(PharmacyShop, on_delete=models.CASCADE, null=True, blank=True)
    
    # Delivery features
    is_delivery_available = models.BooleanField(default=True)
    delivery_time_minutes = models.IntegerField(default=60)
    is_emergency_available = models.BooleanField(default=False)
    storage_temperature = models.CharField(max_length=50, null=True, blank=True)
    
    # Marketplace features
    is_marketplace_active = models.BooleanField(default=True)
    supplier_name = models.CharField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        return str(self.name)

class MedicinePrice(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    pharmacy_shop = models.ForeignKey(PharmacyShop, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    stock_quantity = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['medicine', 'pharmacy_shop']
    
    def get_discounted_price(self):
        return self.price * (1 - self.discount_percentage / 100)
    
    def __str__(self):
        return f"{self.medicine.name} - {self.pharmacy_shop.name} - ${self.price}"
    

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    item = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    purchased = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.quantity} X {self.item}'
    
    # Each product total
    def get_total(self):
        total = self.item.price * self.quantity
        float_total = format(total, '0.2f')
        return float_total
    

class Order(models.Model):
    # id
    orderitems = models.ManyToManyField(Cart)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=200, blank=True, null=True)
    trans_ID = models.CharField(max_length=200, blank=True, null=True)

    # Subtotal
    def get_totals(self):
        total = 0 
        for order_item in self.orderitems.all():
            total += float(order_item.get_total())
        return total
    
    # Count Cart Items
    def count_cart_items(self):
        return self.orderitems.count()
    
    # Stock Calculation
    def stock_quantity_decrease(self):
        for order_item in self.orderitems.all():
            decrease_stock= order_item.item.stock_quantity - order_item.quantity
            order_item.item.stock_quantity = decrease_stock 
            order_item.item.stock_quantity.save()
            return decrease_stock
    
    # TOTAL
    def final_bill(self):
        delivery_price= 40.00
        Bill = self.get_totals()+ delivery_price
        float_Bill = format(Bill, '0.2f')
        return float_Bill
    
