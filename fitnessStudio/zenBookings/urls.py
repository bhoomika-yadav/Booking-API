from django.urls import path
from . import views

urlpatterns = [
    path('classes/', views.get_classes, name='classes-list'),
    path('', views.book_class, name='book-class'),
    path('bookings/', views.get_bookings, name='bookings-list'),
]
