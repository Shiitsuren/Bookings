from django.contrib import admin
from .models import WeeklyAvailability, Booking

from .models import APIToken

@admin.register(APIToken)
class APITokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'key', 'created_at', 'description')

@admin.register(WeeklyAvailability)
class WeeklyAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('user', 'day_of_week', 'start_time', 'end_time')
    list_filter = ('user', 'day_of_week')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('guest_name', 'guest_email', 'user', 'date', 'start_time', 'end_time', 'duration')
    list_filter = ('user', 'date', 'duration')
