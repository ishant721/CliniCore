from django.contrib import admin

# Register your models here.
# # we are in same file path --> .models

from .models import Doctor_Information, Appointment, Report, Prescription, Education, Experience, Specimen, Test,Prescription_medicine,Prescription_test,testCart,testOrder, Doctor_review

class DoctorInformationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'department', 'specialization', 'latitude', 'longitude')
    fieldsets = (
        (None, {
            'fields': ('user', 'name', 'username', 'gender', 'description', 'department', 'department_name', 'specialization', 'featured_image', 'certificate_image', 'email', 'phone_number', 'nid', 'visiting_hour', 'consultation_fee', 'report_fee', 'dob', 'register_status', 'hospital_name')
        }),
        ('Location Information', {
            'fields': ('latitude', 'longitude')
        }),
        ('Education', {
            'fields': ('institute', 'degree', 'completion_year')
        }),
        ('Work Experience', {
            'fields': ('work_place', 'designation', 'start_year', 'end_year')
        }),
    )
    search_fields = ('name', 'email', 'department', 'specialization__specialization_name')
    list_filter = ('department', 'specialization', 'register_status')

admin.site.register(Doctor_Information, DoctorInformationAdmin) # Register with custom admin class
admin.site.register(Appointment)
admin.site.register(Education)
admin.site.register(Experience)
admin.site.register(Report)
admin.site.register(Prescription)
admin.site.register(Test)
admin.site.register(Specimen)
admin.site.register(Prescription_medicine)
admin.site.register(Prescription_test)
admin.site.register(testCart)
admin.site.register(testOrder)
admin.site.register(Doctor_review)
