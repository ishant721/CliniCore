import email
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
# from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from hospital.models import Patient
from pharmacy.models import Medicine, Cart, Order
from .utils import searchMedicines
from django.views.decorators.csrf import csrf_exempt

# Import necessary models for medicine_price_comparison and order_medicine
from pharmacy.models import MedicinePrice, PharmacyShop

# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver


# Create your views here.

# function to return views for the urls

@csrf_exempt
@login_required(login_url="unified-login")
def pharmacy_single_product(request,pk):
     if request.user.is_authenticated and request.user.is_patient:

        patient = Patient.objects.get(user=request.user)
        medicines = Medicine.objects.get(serial_number=pk)
        orders = Order.objects.filter(user=request.user, ordered=False)
        carts = Cart.objects.filter(user=request.user, purchased=False)
        if carts.exists() and orders.exists():
            order = orders[0]
            context = {'patient': patient, 'medicines': medicines,'carts': carts,'order': order, 'orders': orders}
            return render(request, 'pharmacy/product-single.html',context)
        else:
            context = {'patient': patient, 'medicines': medicines,'carts': carts,'orders': orders}
            return render(request, 'pharmacy/product-single.html',context)
     else:
        logout(request)
        messages.error(request, 'Not Authorized')
        return render(request, 'patient-login.html')  

@csrf_exempt
@login_required(login_url="unified-login")
def pharmacy_shop(request):
    if request.user.is_authenticated and request.user.is_patient:

        patient = Patient.objects.get(user=request.user)
        medicines = Medicine.objects.all()
        orders = Order.objects.filter(user=request.user, ordered=False)
        carts = Cart.objects.filter(user=request.user, purchased=False)

        medicines, search_query = searchMedicines(request)

        if carts.exists() and orders.exists():
            order = orders[0]
            context = {'patient': patient, 'medicines': medicines,'carts': carts,'order': order, 'orders': orders, 'search_query': search_query}
            return render(request, 'Pharmacy/shop.html', context)
        else:
            context = {'patient': patient, 'medicines': medicines,'carts': carts,'orders': orders, 'search_query': search_query}
            return render(request, 'Pharmacy/shop.html', context)

    else:
        logout(request)
        messages.error(request, 'Not Authorized')
        return render(request, 'patient-login.html')  

@csrf_exempt
@login_required(login_url="unified-login")
def checkout(request):
    return render(request, 'pharmacy/checkout.html')

@csrf_exempt
@login_required(login_url="unified-login")
def add_to_cart(request, pk):
    if request.user.is_authenticated and request.user.is_patient:

        patient = Patient.objects.get(user=request.user)
        medicines = Medicine.objects.all()

        item = get_object_or_404(Medicine, pk=pk)
        order_item = Cart.objects.get_or_create(item=item, user=request.user, purchased=False)
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.orderitems.filter(item=item).exists():
                order_item[0].quantity += 1
                order_item[0].save()
                # messages.warning(request, "This item quantity was updated!")
                context = {'patient': patient,'medicines': medicines, 'order': order}
                return render(request, 'pharmacy/shop.html', context)

            else:
                order.orderitems.add(order_item[0])
                # messages.warning(request, "This item is added to your cart!")
                context = {'patient': patient,'medicines': medicines,'order': order}
                return render(request, 'pharmacy/shop.html', context)
        else:
            order = Order(user=request.user)
            order.save()
            order.orderitems.add(order_item[0])
            # messages.warning(request, "This item is added to your cart!")
            context = {'patient': patient,'medicines': medicines,'order': order}
            return render(request, 'pharmacy/shop.html', context)
    else:
        logout(request)
        messages.error(request, 'Not Authorized')
        return render(request, 'patient-login.html')  

@csrf_exempt
@login_required(login_url="unified-login")
def cart_view(request):
    if request.user.is_authenticated and request.user.is_patient:

        patient = Patient.objects.get(user=request.user)
        medicines = Medicine.objects.all()

        carts = Cart.objects.filter(user=request.user, purchased=False)
        orders = Order.objects.filter(user=request.user, ordered=False)
        if carts.exists() and orders.exists():
            order = orders[0]
            context = {'carts': carts,'order': order}
            return render(request, 'Pharmacy/cart.html', context)
        else:
            messages.warning(request, "You don't have any item in your cart!")
            context = {'patient': patient,'medicines': medicines}
            return render(request, 'pharmacy/shop.html', context)
    else:
        logout(request)
        messages.info(request, 'Not Authorized')
        return render(request, 'patient-login.html') 

@csrf_exempt
@login_required(login_url="unified-login")
def remove_from_cart(request, pk):
    if request.user.is_authenticated and request.user.is_patient:

        patient = Patient.objects.get(user=request.user)
        medicines = Medicine.objects.all()
        carts = Cart.objects.filter(user=request.user, purchased=False)

        item = get_object_or_404(Medicine, pk=pk)
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.orderitems.filter(item=item).exists():
                order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
                order.orderitems.remove(order_item)
                order_item.delete()
                messages.warning(request, "This item was remove from your cart!")
                context = {'carts': carts,'order': order}
                return render(request, 'Pharmacy/cart.html', context)
            else:
                messages.info(request, "This item was not in your cart")
                context = {'patient': patient,'medicines': medicines}
                return render(request, 'pharmacy/shop.html', context)
        else:
            messages.info(request, "You don't have an active order")
            context = {'patient': patient,'medicines': medicines}
            return render(request, 'pharmacy/shop.html', context)
    else:
        logout(request)
        messages.error(request, 'Not Authorized')
        return render(request, 'patient-login.html') 


@csrf_exempt
@login_required(login_url="unified-login")
def increase_cart(request, pk):
    if request.user.is_authenticated and request.user.is_patient:

        patient = Patient.objects.get(user=request.user)
        medicines = Medicine.objects.all()
        carts = Cart.objects.filter(user=request.user, purchased=False)
        item = get_object_or_404(Medicine, pk=pk)
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.orderitems.filter(item=item).exists():
                order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
                if order_item.quantity >= 1:
                    order_item.quantity += 1
                    order_item.save()
                    messages.warning(request, f"{item.name} quantity has been updated")
                    context = {'carts': carts,'order': order}
                    return render(request, 'Pharmacy/cart.html', context)
            else:
                messages.warning(request, f"{item.name} is not in your cart")
                context = {'patient': patient,'medicines': medicines}
                return render(request, 'pharmacy/shop.html', context)
        else:
            messages.warning(request, "You don't have an active order")
            context = {'patient': patient,'medicines': medicines}
            return render(request, 'pharmacy/shop.html', context)
    else:
        logout(request)
        messages.error(request, 'Not Authorized')
        return render(request, 'patient-login.html') 


@csrf_exempt
@login_required(login_url="unified-login")
def decrease_cart(request, pk):
    if request.user.is_authenticated and request.user.is_patient:

        patient = Patient.objects.get(user=request.user)
        medicines = Medicine.objects.all()
        carts = Cart.objects.filter(user=request.user, purchased=False)
        item = get_object_or_404(Medicine, pk=pk)
        order_qs = Order.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.orderitems.filter(item=item).exists():
                order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
                if order_item.quantity > 1:
                    order_item.quantity -= 1
                    order_item.save()
                    messages.warning(request, f"{item.name} quantity has been updated")
                    context = {'carts': carts,'order': order}
                    return render(request, 'Pharmacy/cart.html', context)
                else:
                    order.orderitems.remove(order_item)
                    order_item.delete()
                    messages.warning(request, f"{item.name} item has been removed from your cart")
                    context = {'carts': carts,'order': order}
                    return render(request, 'Pharmacy/cart.html', context)
            else:
                messages.info(request, f"{item.name} is not in your cart")
                context = {'patient': patient,'medicines': medicines}
                return render(request, 'pharmacy/shop.html', context)
        else:
            messages.info(request, "You don't have an active order")
            context = {'patient': patient,'medicines': medicines}
            return render(request, 'pharmacy/shop.html', context)
    else:
        logout(request)
        messages.error(request, 'Not Authorized')
        return render(request, 'patient-login.html') 
# Create your views here.
import json
from django.db.models import Min, Q
from django.core.paginator import Paginator
from doctor.models import Prescription_medicine

@csrf_exempt
@login_required(login_url="unified-login")
def medicine_list(request):
    """Display list of all available medicines"""
    medicines = Medicine.objects.all()

    context = {
        'medicines': medicines,
        'total_medicines': medicines.count(),
    }

    return render(request, 'pharmacy/medicine_list.html', context)

@csrf_exempt
@login_required(login_url="unified-login")
def medicine_price_comparison(request):
    """Compare prices of medicines across different pharmacy shops"""
    if request.user.is_patient:
        patient = Patient.objects.get(user=request.user)

        # Get prescription medicines for the patient
        prescription_medicines = Prescription_medicine.objects.filter(
            prescription__patient=patient,
            is_ordered=False
        )

        comparison_data = []

        for presc_med in prescription_medicines:
            # Find medicines with similar names or generic names
            medicines = Medicine.objects.filter(
                Q(name__icontains=presc_med.medicine_name) |
                Q(generic_name__icontains=presc_med.medicine_name)
            ).filter(is_marketplace_active=True)

            medicine_prices = []
            for medicine in medicines:
                prices = MedicinePrice.objects.filter(
                    medicine=medicine,
                    is_available=True,
                    stock_quantity__gt=0
                ).select_related('pharmacy_shop').order_by('price')

                for price_obj in prices:
                    medicine_prices.append({
                        'medicine': medicine,
                        'pharmacy_shop': price_obj.pharmacy_shop,
                        'price': price_obj.price,
                        'discounted_price': price_obj.get_discounted_price(),
                        'discount_percentage': price_obj.discount_percentage,
                        'stock_quantity': price_obj.stock_quantity,
                        'delivery_time': price_obj.pharmacy_shop.average_delivery_time,
                        'rating': price_obj.pharmacy_shop.rating,
                    })

            if medicine_prices:
                # Sort by discounted price
                medicine_prices.sort(key=lambda x: x['discounted_price'])
                comparison_data.append({
                    'prescription_medicine': presc_med,
                    'available_options': medicine_prices
                })

        context = {
            'patient': patient,
            'comparison_data': comparison_data
        }

        return render(request, 'pharmacy/medicine_comparison.html', context)

    return redirect('unified-login')

@csrf_exempt
@login_required(login_url="unified-login")
def order_medicine(request):
    """Handle medicine ordering from selected pharmacy"""
    if request.method == 'POST' and request.user.is_patient:
        patient = Patient.objects.get(user=request.user)

        medicine_id = request.POST.get('medicine_id')
        pharmacy_shop_id = request.POST.get('pharmacy_shop_id')
        quantity = int(request.POST.get('quantity', 1))
        prescription_medicine_id = request.POST.get('prescription_medicine_id')

        try:
            medicine = Medicine.objects.get(serial_number=medicine_id)
            pharmacy_shop = PharmacyShop.objects.get(shop_id=pharmacy_shop_id)
            medicine_price = MedicinePrice.objects.get(
                medicine=medicine,
                pharmacy_shop=pharmacy_shop
            )

            # Create order
            order = Order.objects.create(
                user=request.user,
                ordered=False
            )

            # Create cart item
            cart_item = Cart.objects.create(
                user=request.user,
                item=medicine,
                quantity=quantity,
                purchased=False
            )

            order.orderitems.add(cart_item)

            # Update prescription medicine status
            if prescription_medicine_id:
                presc_med = Prescription_medicine.objects.get(
                    medicine_id=prescription_medicine_id
                )
                presc_med.is_ordered = True
                presc_med.order_status = 'ordered'
                presc_med.save()

            messages.success(request, f'Medicine ordered successfully from {pharmacy_shop.name}!')
            return redirect('medicine-comparison')

        except Exception as e:
            messages.error(request, f'Error placing order: {str(e)}')
            return redirect('medicine-comparison')

    return redirect('unified-login')

@csrf_exempt
@login_required(login_url="unified-login")
def pharmacy_shop_list(request):
    """List all verified pharmacy shops"""
    shops = PharmacyShop.objects.filter(is_verified=True).order_by('-rating')

    # Add search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        shops = shops.filter(
            Q(name__icontains=search_query) |
            Q(address__icontains=search_query)
        )

    # Pagination
    paginator = Paginator(shops, 12)
    page_number = request.GET.get('page')
    shops = paginator.get_page(page_number)

    context = {
        'shops': shops,
        'search_query': search_query
    }

    return render(request, 'pharmacy/pharmacy_shops.html', context)

@csrf_exempt
@login_required(login_url="unified-login")
def pharmacy_shop_detail(request, shop_id):
    """Show details of a specific pharmacy shop"""
    shop = PharmacyShop.objects.get(shop_id=shop_id)
    medicines = Medicine.objects.filter(
        pharmacy_shop=shop,
        is_marketplace_active=True
    ).order_by('name')

    # Get medicine prices for this shop
    medicine_prices = MedicinePrice.objects.filter(
        pharmacy_shop=shop,
        is_available=True
    ).select_related('medicine')

    context = {
        'shop': shop,
        'medicines': medicines,
        'medicine_prices': medicine_prices
    }

    return render(request, 'pharmacy/pharmacy_shop_detail.html', context)