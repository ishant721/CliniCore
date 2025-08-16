
from django.urls import path
from . import views

app_name = 'marketplace'

urlpatterns = [
    # Main marketplace pages
    path('', views.marketplace_home, name='home'),
    path('providers/', views.service_providers_list, name='providers_list'),
    path('provider/<int:provider_id>/', views.provider_detail, name='provider_detail'),
    
    # Order management
    path('order/create/', views.create_order, name='create_order'),
    path('orders/', views.my_orders, name='my_orders'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('order/<int:order_id>/track/', views.track_order, name='track_order'),
    path('order/<int:order_id>/cancel/', views.cancel_order, name='cancel_order'),
    
    # Provider dashboard
    path('provider/dashboard/', views.provider_dashboard, name='provider_dashboard'),
    path('provider/status/update/', views.update_provider_status, name='update_provider_status'),
    path('provider/order/<int:order_id>/manage/', views.manage_order, name='manage_order'),
    
    # AJAX endpoints
    path('api/search/', views.search_providers_ajax, name='search_providers_ajax'),
    path('api/provider/<int:provider_id>/availability/', views.get_provider_availability, name='provider_availability'),
]
