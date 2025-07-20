from django.urls import path
from . import views

urlpatterns = [
    path('availability/', views.WeeklyAvailabilityListCreateView.as_view(), name='availability-list-create'),
    path('bookings/', views.BookingListCreateView.as_view(), name='booking-list-create'),
]
