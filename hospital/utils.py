from django.db.models import Q
from .models import Patient, User, Hospital_Information
from doctor.models import Doctor_Information, Appointment
from hospital_admin.models import hospital_department, specialization, service
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import random
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.conf import settings


def searchDoctors(request):
    
    search_query = ''
    
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
        
    #skills = Skill.objects.filter(name__icontains=search_query)
    
    doctors = Doctor_Information.objects.filter(register_status='Accepted').distinct().filter(
        Q(name__icontains=search_query) |
        Q(hospital_name__name__icontains=search_query) |  
        Q(department__icontains=search_query))
    
    return doctors, search_query


def searchHospitals(request):
    
    search_query = ''
    
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
        
    
    hospitals = Hospital_Information.objects.distinct().filter(Q(name__icontains=search_query))
    
    return hospitals, search_query


def paginateHospitals(request, hospitals, results):

    page = request.GET.get('page')
    paginator = Paginator(hospitals, results)

    try:
        hospitals = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        hospitals = paginator.page(page)
    except EmptyPage:
        # display last page if page is out of range
        page = paginator.num_pages
        hospitals = paginator.page(page)
        
    
    # if there are many pages, we will see some at a time in the pagination bar (range window)
    # leftIndex(left button) = current page no. - 4 
    leftIndex = (int(page) - 4)
    if leftIndex < 1:
        # if leftIndex is less than 1, we will start from 1
        leftIndex = 1

    rightIndex = (int(page) + 5)
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)
    # return custom_range, projects, paginator
    return custom_range, hospitals


# def searchDepartmentDoctors(request, pk):
    
#     search_query = ''
    
#     if request.GET.get('search_query'):
#         search_query = request.GET.get('search_query')
        
    
#     departments = hospital_department.object.filter(hospital_department_id=pk).filter(
#         Q(doctor__name__icontains=search_query) |  
#         Q(doctor__department__icontains=search_query))
    
#     return departments, search_query

def searchDepartmentDoctors(request, pk):
    
    search_query = ''
    
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
        
    departments = hospital_department.objects.get(hospital_department_id=pk)
    
    doctors = Doctor_Information.objects.filter(department_name=departments).filter(
        Q(name__icontains=search_query))
    
    # doctors = Doctor_Information.objects.filter(department_name=departments).filter(
    #     Q(name__icontains=search_query) |
    #     Q(specialization_name__name__icontains=search_query))
    
    return doctors, search_query



# products = Products.objects.filter(price__range=[10, 100])

def send_otp_email(user, otp_type="verification"):
    """
    Generates and sends an OTP to the user's email.
    otp_type can be 'verification' for registration or 'reset_password' for password reset.
    """
    otp_code = str(random.randint(100000, 999999))
    user.otp_code = otp_code
    user.otp_expires_at = datetime.now() + timedelta(minutes=5) # OTP valid for 5 minutes
    user.save()

    subject = f'Your OTP for CliniCore {otp_type.replace("_", " ").title()}'
    message = f'''Hi {user.username},

Your One-Time Password (OTP) for {otp_type.replace("_", " ")} is: {otp_code}

This OTP is valid for 5 minutes. Please do not share it with anyone.

Thanks,
CliniCore Team'''
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email]

    try:
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        return True
    except Exception as e:
        print(f"Error sending OTP email: {e}")
        return False