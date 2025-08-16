
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
import math

from hospital.models import Patient
from doctor.models import Doctor_Information
from pharmacy.models import Medicine
from .models import ServiceProvider, MarketplaceOrder, DeliveryPartner

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two points using Haversine formula"""
    R = 6371  # Earth's radius in kilometers
    
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    return R * c

@login_required(login_url="login")
def marketplace_home(request):
    """Main marketplace dashboard"""
    if not hasattr(request.user, 'patient'):
        messages.error(request, 'Patient profile required for marketplace access')
        return redirect('patient-register')
    
    patient = request.user.patient
    
    # Get nearby service providers
    nearby_doctors = Doctor_Information.objects.filter(
        is_marketplace_active=True,
        latitude__isnull=False,
        longitude__isnull=False
    )[:6]
    
    # Get available medicines
    available_medicines = Medicine.objects.filter(
        is_marketplace_active=True,
        stock_quantity__gt=0
    )[:8]
    
    # Recent orders
    recent_orders = MarketplaceOrder.objects.filter(
        user=request.user
    ).order_by('-created_at')[:5]
    
    context = {
        'patient': patient,
        'nearby_doctors': nearby_doctors,
        'available_medicines': available_medicines,
        'recent_orders': recent_orders,
    }
    return render(request, 'marketplace/home.html', context)

@login_required(login_url="login")
def find_doctors(request):
    """Find doctors with filters and location"""
    if not hasattr(request.user, 'patient'):
        messages.error(request, 'Patient profile required')
        return redirect('patient-register')
    
    patient = request.user.patient
    
    # Get filters from request
    specialty = request.GET.get('specialty', '')
    consultation_type = request.GET.get('consultation_type', 'all')
    max_distance = request.GET.get('max_distance', '10')
    availability = request.GET.get('availability', 'all')
    
    # Base query
    doctors = Doctor_Information.objects.filter(
        is_marketplace_active=True,
        register_status='approved'
    )
    
    # Apply filters
    if specialty:
        doctors = doctors.filter(department__icontains=specialty)
    
    if consultation_type == 'online':
        doctors = doctors.filter(online_consultation_available=True)
    elif consultation_type == 'home_visit':
        doctors = doctors.filter(home_visit_available=True)
    elif consultation_type == 'instant':
        doctors = doctors.filter(instant_booking_available=True)
    
    if availability == 'now':
        doctors = doctors.filter(
            visiting_hour__isnull=False
        )
    
    # Calculate distances if patient has location
    doctors_with_distance = []
    for doctor in doctors:
        if doctor.latitude and doctor.longitude:
            # For demo purposes, using hospital location as patient location
            # In real implementation, get patient's current location
            distance = 5  # Default distance
            doctors_with_distance.append({
                'doctor': doctor,
                'distance': distance,
                'estimated_time': distance * 2  # Rough estimate
            })
    
    # Sort by distance
    doctors_with_distance.sort(key=lambda x: x['distance'])
    
    context = {
        'patient': patient,
        'doctors_with_distance': doctors_with_distance,
        'specialty': specialty,
        'consultation_type': consultation_type,
        'max_distance': max_distance,
        'availability': availability,
    }
    return render(request, 'marketplace/find_doctors.html', context)

@login_required(login_url="login")
def medicine_delivery(request):
    """Medicine delivery marketplace"""
    if not hasattr(request.user, 'patient'):
        messages.error(request, 'Patient profile required')
        return redirect('patient-register')
    
    patient = request.user.patient
    
    # Get filters
    category = request.GET.get('category', 'all')
    search_query = request.GET.get('search', '')
    prescription_required = request.GET.get('prescription_required', 'all')
    
    # Base query
    medicines = Medicine.objects.filter(
        is_marketplace_active=True,
        stock_quantity__gt=0
    )
    
    # Apply filters
    if category != 'all':
        medicines = medicines.filter(medicine_category=category)
    
    if search_query:
        medicines = medicines.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    if prescription_required != 'all':
        medicines = medicines.filter(Prescription_reqiuired=prescription_required)
    
    # Group by category for better display
    medicine_categories = medicines.values_list('medicine_category', flat=True).distinct()
    
    context = {
        'patient': patient,
        'medicines': medicines,
        'medicine_categories': medicine_categories,
        'category': category,
        'search_query': search_query,
        'prescription_required': prescription_required,
    }
    return render(request, 'marketplace/medicine_delivery.html', context)

@login_required(login_url="login")
def book_consultation(request, doctor_id):
    """Book a consultation with a doctor"""
    if not hasattr(request.user, 'patient'):
        messages.error(request, 'Patient profile required')
        return redirect('patient-register')
    
    doctor = get_object_or_404(Doctor_Information, doctor_id=doctor_id)
    patient = request.user.patient
    
    if request.method == 'POST':
        consultation_type = request.POST.get('consultation_type')
        preferred_time = request.POST.get('preferred_time')
        message = request.POST.get('message', '')
        
        # Calculate fees
        if consultation_type == 'online':
            fee = doctor.online_consultation_fee or doctor.consultation_fee
        elif consultation_type == 'home_visit':
            fee = doctor.home_visit_fee or (doctor.consultation_fee + 200)
        else:
            fee = doctor.consultation_fee
        
        # Create marketplace order
        estimated_time = timezone.now() + timedelta(minutes=doctor.average_response_time)
        
        order = MarketplaceOrder.objects.create(
            user=request.user,
            service_provider_id=1,  # Will be linked to doctor's service provider
            order_type='consultation',
            delivery_latitude=0,  # Patient's location
            delivery_longitude=0,
            delivery_address=patient.address or 'Home',
            subtotal=fee,
            delivery_fee=0 if consultation_type == 'online' else 50,
            total_amount=fee + (0 if consultation_type == 'online' else 50),
            estimated_delivery_time=estimated_time
        )
        
        messages.success(request, f'Consultation booking request sent to Dr. {doctor.name}')
        return redirect('marketplace_orders')
    
    context = {
        'doctor': doctor,
        'patient': patient,
    }
    return render(request, 'marketplace/book_consultation.html', context)

@login_required(login_url="login")
def marketplace_orders(request):
    """View all marketplace orders"""
    if not hasattr(request.user, 'patient'):
        messages.error(request, 'Patient profile required')
        return redirect('patient-register')
    
    orders = MarketplaceOrder.objects.filter(
        user=request.user
    ).order_by('-created_at')
    
    context = {
        'orders': orders,
    }
    return render(request, 'marketplace/orders.html', context)

@login_required(login_url="login")
def track_order(request, order_id):
    """Track a specific order"""
    order = get_object_or_404(MarketplaceOrder, order_id=order_id, user=request.user)
    
    # Mock tracking data
    tracking_steps = [
        {'step': 'Order Placed', 'completed': True, 'time': order.created_at},
        {'step': 'Confirmed', 'completed': order.status in ['confirmed', 'preparing', 'out_for_delivery', 'delivered'], 'time': None},
        {'step': 'Preparing', 'completed': order.status in ['preparing', 'out_for_delivery', 'delivered'], 'time': None},
        {'step': 'Out for Delivery', 'completed': order.status in ['out_for_delivery', 'delivered'], 'time': None},
        {'step': 'Delivered', 'completed': order.status == 'delivered', 'time': order.actual_delivery_time},
    ]
    
    context = {
        'order': order,
        'tracking_steps': tracking_steps,
    }
    return render(request, 'marketplace/track_order.html', context)
