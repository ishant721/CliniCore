from django.contrib import admin

# Register your models here.
# # we are in same file path --> .models

from .models import Hospital_Information, Patient, User

class HospitalInformationAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone_number', 'hospital_type', 'latitude', 'longitude')
    fieldsets = (
        (None, {
            'fields': ('name', 'address', 'phone_number', 'hospital_type', 'featured_image', 'description', 'email')
        }),
        ('Location Information', {
            'fields': ('latitude', 'longitude')
        }),
        ('Bed Information', {
            'fields': ('general_bed_no', 'available_icu_no', 'regular_cabin_no', 'emergency_cabin_no', 'vip_cabin_no')
        }),
    )
    search_fields = ('name', 'address', 'hospital_type')
    list_filter = ('hospital_type',)

admin.site.register(User)
admin.site.register(Hospital_Information, HospitalInformationAdmin)
admin.site.register(Patient)

