
from django.contrib import admin
from .models import ServiceProvider, DeliveryPartner, MarketplaceOrder

@admin.register(ServiceProvider)
class ServiceProviderAdmin(admin.ModelAdmin):
    list_display = ['name', 'service_type', 'availability_status', 'rating', 'created_at']
    list_filter = ['service_type', 'availability_status']
    search_fields = ['name']

@admin.register(DeliveryPartner)
class DeliveryPartnerAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'vehicle_type', 'rating', 'total_deliveries']
    list_filter = ['status', 'vehicle_type', 'is_verified']
    search_fields = ['name', 'phone_number']

@admin.register(MarketplaceOrder)
class MarketplaceOrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'user', 'order_type', 'status', 'total_amount', 'created_at']
    list_filter = ['order_type', 'status', 'priority']
    search_fields = ['order_id', 'user__username']
    readonly_fields = ['created_at']
