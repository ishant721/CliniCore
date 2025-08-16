
from django.urls import path
from . import views

urlpatterns = [
    path('', views.marketplace_home, name='marketplace_home'),
    path('doctors/', views.find_doctors, name='marketplace_doctors'),
    path('medicine-delivery/', views.medicine_delivery, name='marketplace_medicine'),
    path('book-consultation/<int:doctor_id>/', views.book_consultation, name='book_consultation'),
    path('orders/', views.marketplace_orders, name='marketplace_orders'),
    path('track/<int:order_id>/', views.track_order, name='track_order'),
]
