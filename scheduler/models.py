
from django.db import models
from django.contrib.auth.models import User

class APIToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='api_tokens')
    key = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.key}"

class WeeklyAvailability(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='availabilities')
    day_of_week = models.IntegerField(choices=[(i, day) for i, day in enumerate(['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'])])
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        unique_together = ('user', 'day_of_week', 'start_time', 'end_time')
        ordering = ['user', 'day_of_week', 'start_time']

    def __str__(self):
        return f"{self.user.username} - {self.get_day_of_week_display()} {self.start_time}-{self.end_time}"

class Booking(models.Model):
    guest_name = models.CharField(max_length=100)
    guest_email = models.EmailField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    duration = models.IntegerField(choices=[(15, '15 min'), (30, '30 min'), (45, '45 min'), (60, '1 hour')])

    class Meta:
        unique_together = ('user', 'date', 'start_time', 'end_time')
        ordering = ['user', 'date', 'start_time']

    def __str__(self):
        return f"{self.guest_name} booking with {self.user.username} on {self.date} {self.start_time}-{self.end_time}"
