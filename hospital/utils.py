from django.db.models import Q
from .models import Patient, User, Hospital_Information
from doctor.models import Doctor_Information, Appointment,Report, Specimen, Test, Prescription, Prescription_medicine, Prescription_test
from hospital_admin.models import hospital_department, specialization, service
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import random

from django.core.mail import send_mail
from django.conf import settings
import secrets
import string
from django.utils import timezone
from datetime import timedelta
from math import radians, sin, cos, sqrt, atan2

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of Earth in kilometers

    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance


def searchDoctors(request, user_lat=None, user_lon=None, radius=None):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    doctors = Doctor_Information.objects.filter(register_status='Accepted').distinct().filter(
        Q(name__icontains=search_query) |
        Q(hospital_name__name__icontains=search_query) |
        Q(department__icontains=search_query)
    )

    if user_lat and user_lon and radius:
        try:
            user_lat = float(user_lat)
            user_lon = float(user_lon)
            radius = float(radius)
            
            doctors_with_distance = []
            for doctor in doctors:
                if doctor.latitude is not None and doctor.longitude is not None:
                    distance = haversine(user_lat, user_lon, float(doctor.latitude), float(doctor.longitude))
                    if distance <= radius:
                        doctor.distance = round(distance, 2) # Attach distance to object
                        doctors_with_distance.append(doctor)
            doctors = sorted(doctors_with_distance, key=lambda x: x.distance) # Sort by distance
        except ValueError:
            pass

    return doctors, search_query


def searchHospitals(request, user_lat=None, user_lon=None, radius=None):

    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    hospitals = Hospital_Information.objects.distinct().filter(Q(name__icontains=search_query))

    if user_lat and user_lon and radius:
        try:
            user_lat = float(user_lat)
            user_lon = float(user_lon)
            radius = float(radius)

            hospitals_with_distance = []
            for hospital in hospitals:
                if hospital.latitude is not None and hospital.longitude is not None:
                    distance = haversine(user_lat, user_lon, float(hospital.latitude), float(hospital.longitude))
                    if distance <= radius:
                        hospital.distance = round(distance, 2) # Attach distance to object
                        hospitals_with_distance.append(hospital)
            hospitals = sorted(hospitals_with_distance, key=lambda x: x.distance) # Sort by distance
        except ValueError:
            pass

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

def generate_backup_codes(count=8):
    """Generate backup codes for 2FA"""
    codes = []
    for _ in range(count):
        code = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(8))
        codes.append(code)
    return codes

def send_otp_email(user, purpose="registration"):
    """
    Send OTP email to user for various purposes
    """
    try:
        # Generate 6-digit OTP
        otp_code = str(random.randint(100000, 999999))

        # Set OTP expiration time based on purpose
        if purpose == "two_factor_authentication":
            otp_expires_at = timezone.now() + timedelta(minutes=5)  # Shorter for 2FA
        else:
            otp_expires_at = timezone.now() + timedelta(minutes=15)

        # Save OTP to user
        user.otp_code = otp_code
        user.otp_expires_at = otp_expires_at
        user.save()

        # Prepare email content based on purpose
        if purpose == "registration":
            subject = "HealthStack - Account Verification"
            template_message = f"""
            Welcome to HealthStack!

            Your verification code is: {otp_code}

            This code will expire in 15 minutes. Please do not share this code with anyone.

            If you didn't request this verification, please ignore this email.
            """
        elif purpose == "password_reset":
            subject = "HealthStack - Password Reset"
            template_message = f"""
            Password Reset Request

            Your password reset code is: {otp_code}

            This code will expire in 15 minutes. Please do not share this code with anyone.

            If you didn't request a password reset, please ignore this email and ensure your account is secure.
            """
        elif purpose == "two_factor_authentication":
            subject = "HealthStack - Two-Factor Authentication"
            template_message = f"""
            Two-Factor Authentication Code

            Your 2FA code is: {otp_code}

            This code will expire in 5 minutes. Please do not share this code with anyone.

            If you didn't attempt to log in, please secure your account immediately.
            """
        else:
            subject = "HealthStack - Verification Code"
            template_message = f"""
            Verification Code

            Your verification code is: {otp_code}

            This code will expire in 15 minutes. Please do not share this code with anyone.
            """

        # Send email
        send_mail(
            subject,
            template_message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        return True

    except Exception as e:
        print(f"Error sending OTP email: {e}")
        return False