
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import ServiceProvider, MarketplaceOrder, DeliveryPartner
from doctor.models import Doctor_Information
from pharmacy.models import Medicine, Pharmacist
from hospital.models import Patient, User
import json
from datetime import datetime, timedelta
from django.utils import timezone

def marketplace_home(request):
    """Main marketplace homepage showing available services"""
    # Get featured service providers
    featured_doctors = ServiceProvider.objects.filter(
        service_type='consultation',
        availability_status='available'
    )[:6]
    
    featured_medicines = ServiceProvider.objects.filter(
        service_type='medicine_delivery',
        availability_status='available'
    )[:6]
    
    # Get quick stats
    total_doctors = ServiceProvider.objects.filter(service_type='consultation').count()
    total_pharmacies = ServiceProvider.objects.filter(service_type='medicine_delivery').count()
    
    context = {
        'featured_doctors': featured_doctors,
        'featured_medicines': featured_medicines,
        'total_doctors': total_doctors,
        'total_pharmacies': total_pharmacies,
    }
    return render(request, 'marketplace/home.html', context)

def service_providers_list(request):
    """List all service providers with filtering"""
    service_type = request.GET.get('type', 'consultation')
    location = request.GET.get('location', '')
    search_query = request.GET.get('search', '')
    
    providers = ServiceProvider.objects.filter(service_type=service_type)
    
    if location:
        # Filter by location - simplified for now
        providers = providers.filter(
            Q(hospital__hospital_address__icontains=location) |
            Q(doctor__work_place__icontains=location)
        )
    
    if search_query:
        providers = providers.filter(
            Q(name__icontains=search_query) |
            Q(doctor__specialization__name__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(providers, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'providers': page_obj,
        'service_type': service_type,
        'location': location,
        'search_query': search_query,
    }
    return render(request, 'marketplace/providers_list.html', context)

def provider_detail(request, provider_id):
    """Detailed view of a service provider"""
    provider = get_object_or_404(ServiceProvider, provider_id=provider_id)
    
    # Get related medicines if pharmacy
    medicines = []
    if provider.service_type == 'medicine_delivery' and provider.pharmacist:
        medicines = Medicine.objects.filter(is_marketplace_active=True)[:10]
    
    context = {
        'provider': provider,
        'medicines': medicines,
    }
    return render(request, 'marketplace/provider_detail.html', context)

@login_required(login_url="unified-login")
def create_order(request):
    """Create a new marketplace order"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            provider_id = data.get('provider_id')
            delivery_address = data.get('delivery_address')
            delivery_latitude = data.get('delivery_latitude')
            delivery_longitude = data.get('delivery_longitude')
            order_type = data.get('order_type')
            priority = data.get('priority', 'normal')
            
            provider = get_object_or_404(ServiceProvider, provider_id=provider_id)
            
            # Calculate estimated delivery time
            estimated_delivery = timezone.now() + timedelta(minutes=provider.average_delivery_time)
            
            # Calculate total amount
            subtotal = provider.base_fee
            delivery_fee = provider.delivery_fee
            if priority == 'emergency':
                delivery_fee += provider.emergency_fee
            total_amount = subtotal + delivery_fee
            
            # Create order
            order = MarketplaceOrder.objects.create(
                user=request.user,
                service_provider=provider,
                order_type=order_type,
                priority=priority,
                delivery_latitude=delivery_latitude,
                delivery_longitude=delivery_longitude,
                delivery_address=delivery_address,
                subtotal=subtotal,
                delivery_fee=delivery_fee,
                total_amount=total_amount,
                estimated_delivery_time=estimated_delivery,
                status='pending'
            )
            
            return JsonResponse({
                'success': True,
                'order_id': order.order_id,
                'message': 'Order created successfully!'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@login_required(login_url="unified-login")
def my_orders(request):
    """View user's marketplace orders"""
    orders = MarketplaceOrder.objects.filter(user=request.user).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'orders': page_obj,
    }
    return render(request, 'marketplace/my_orders.html', context)

@login_required(login_url="unified-login")
def order_detail(request, order_id):
    """Detailed view of an order"""
    order = get_object_or_404(MarketplaceOrder, order_id=order_id, user=request.user)
    
    context = {
        'order': order,
    }
    return render(request, 'marketplace/order_detail.html', context)

@login_required(login_url="unified-login")
def track_order(request, order_id):
    """Track order status"""
    order = get_object_or_404(MarketplaceOrder, order_id=order_id, user=request.user)
    
    # Get delivery partner location if assigned
    partner_location = None
    if order.delivery_partner:
        partner_location = {
            'latitude': float(order.delivery_partner.current_latitude) if order.delivery_partner.current_latitude else None,
            'longitude': float(order.delivery_partner.current_longitude) if order.delivery_partner.current_longitude else None,
        }
    
    context = {
        'order': order,
        'partner_location': partner_location,
    }
    return render(request, 'marketplace/track_order.html', context)

@login_required(login_url="unified-login")
def cancel_order(request, order_id):
    """Cancel an order"""
    order = get_object_or_404(MarketplaceOrder, order_id=order_id, user=request.user)
    
    if order.status in ['pending', 'confirmed']:
        order.status = 'cancelled'
        order.save()
        messages.success(request, 'Order cancelled successfully!')
    else:
        messages.error(request, 'Order cannot be cancelled at this stage.')
    
    return redirect('marketplace:order_detail', order_id=order_id)

# Provider Dashboard Views
@login_required(login_url="unified-login")
def provider_dashboard(request):
    """Dashboard for service providers"""
    try:
        # Check if user is a doctor
        if hasattr(request.user, 'profile'):
            doctor = request.user.profile
            provider = ServiceProvider.objects.get(doctor=doctor)
        else:
            messages.error(request, 'Access denied. Provider account not found.')
            return redirect('marketplace:home')
        
        # Get recent orders
        recent_orders = MarketplaceOrder.objects.filter(
            service_provider=provider
        ).order_by('-created_at')[:10]
        
        # Get statistics
        total_orders = MarketplaceOrder.objects.filter(service_provider=provider).count()
        pending_orders = MarketplaceOrder.objects.filter(
            service_provider=provider, 
            status='pending'
        ).count()
        completed_orders = MarketplaceOrder.objects.filter(
            service_provider=provider, 
            status='delivered'
        ).count()
        
        context = {
            'provider': provider,
            'recent_orders': recent_orders,
            'total_orders': total_orders,
            'pending_orders': pending_orders,
            'completed_orders': completed_orders,
        }
        return render(request, 'marketplace/provider_dashboard.html', context)
        
    except ServiceProvider.DoesNotExist:
        messages.error(request, 'Provider profile not found.')
        return redirect('marketplace:home')

@login_required(login_url="unified-login")
def update_provider_status(request):
    """Update provider availability status"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            status = data.get('status')
            
            if hasattr(request.user, 'profile'):
                doctor = request.user.profile
                provider = ServiceProvider.objects.get(doctor=doctor)
                provider.availability_status = status
                provider.save()
                
                return JsonResponse({
                    'success': True,
                    'message': f'Status updated to {status}'
                })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})

@login_required(login_url="unified-login")
def manage_order(request, order_id):
    """Manage order status by provider"""
    order = get_object_or_404(MarketplaceOrder, order_id=order_id)
    
    # Check if user owns this provider
    try:
        if hasattr(request.user, 'profile'):
            doctor = request.user.profile
            provider = ServiceProvider.objects.get(doctor=doctor)
            if order.service_provider != provider:
                messages.error(request, 'Access denied.')
                return redirect('marketplace:provider_dashboard')
    except ServiceProvider.DoesNotExist:
        messages.error(request, 'Provider not found.')
        return redirect('marketplace:home')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'confirm':
            order.status = 'confirmed'
            messages.success(request, 'Order confirmed!')
        elif action == 'preparing':
            order.status = 'preparing'
            messages.success(request, 'Order marked as preparing!')
        elif action == 'ready':
            order.status = 'out_for_delivery'
            messages.success(request, 'Order marked as ready for delivery!')
        elif action == 'delivered':
            order.status = 'delivered'
            order.actual_delivery_time = timezone.now()
            messages.success(request, 'Order marked as delivered!')
        
        order.save()
        return redirect('marketplace:manage_order', order_id=order_id)
    
    context = {
        'order': order,
    }
    return render(request, 'marketplace/manage_order.html', context)

# AJAX Views
def search_providers_ajax(request):
    """AJAX search for providers"""
    query = request.GET.get('q', '')
    service_type = request.GET.get('type', 'consultation')
    
    providers = ServiceProvider.objects.filter(
        service_type=service_type,
        name__icontains=query
    )[:10]
    
    results = []
    for provider in providers:
        results.append({
            'id': provider.provider_id,
            'name': provider.name,
            'rating': float(provider.rating),
            'delivery_time': provider.average_delivery_time,
            'base_fee': float(provider.base_fee),
        })
    
    return JsonResponse({'providers': results})

def get_provider_availability(request, provider_id):
    """Get real-time provider availability"""
    provider = get_object_or_404(ServiceProvider, provider_id=provider_id)
    
    return JsonResponse({
        'status': provider.availability_status,
        'estimated_time': provider.average_delivery_time,
    })
