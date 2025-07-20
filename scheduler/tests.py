from django.test import TestCase

from django.test import TestCase
from django.contrib.auth.models import User
from .models import WeeklyAvailability, Booking
from datetime import time, date

class BookingTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        WeeklyAvailability.objects.create(user=self.user, day_of_week=0, start_time=time(9,0), end_time=time(17,0))

    def test_create_valid_booking(self):
        booking = Booking.objects.create(
            guest_name='Guest',
            guest_email='guest@example.com',
            user=self.user,
            date=date(2025, 7, 21),
            start_time=time(10,0),
            end_time=time(10,15),
            duration=15
        )
        self.assertEqual(Booking.objects.count(), 1)

    def test_overlapping_booking(self):
        Booking.objects.create(
            guest_name='Guest1',
            guest_email='g1@example.com',
            user=self.user,
            date=date(2025, 7, 21),
            start_time=time(10,0),
            end_time=time(10,30),
            duration=30
        )
        with self.assertRaises(Exception):
            Booking.objects.create(
                guest_name='Guest2',
                guest_email='g2@example.com',
                user=self.user,
                date=date(2025, 7, 21),
                start_time=time(10,15),
                end_time=time(10,45),
                duration=30
            )
