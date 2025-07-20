from rest_framework import serializers
from .models import WeeklyAvailability, Booking
from django.utils import timezone
from datetime import datetime, timedelta

class WeeklyAvailabilitySerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    day_of_week_display = serializers.CharField(source='get_day_of_week_display', read_only=True)

    class Meta:
        model = WeeklyAvailability
        fields = ['id', 'user', 'day_of_week', 'day_of_week_display', 'start_time', 'end_time']

class BookingSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = self.context.get('user')
        return Booking.objects.create(user=user, **validated_data)
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Booking
        fields = ['id', 'guest_name', 'guest_email', 'user', 'date', 'start_time', 'end_time', 'duration']

    def validate(self, data):
        if data['duration'] not in [15, 30, 45, 60]:
            raise serializers.ValidationError('Invalid duration.')
        start_dt = datetime.combine(data['date'], data['start_time'])
        end_dt = start_dt + timedelta(minutes=data['duration'])
        data['end_time'] = end_dt.time()
        availabilities = WeeklyAvailability.objects.filter(
            user=self.context['user'],
            day_of_week=data['date'].weekday(),
            start_time__lte=data['start_time'],
            end_time__gte=end_dt.time()
        )
        if not availabilities.exists():
            raise serializers.ValidationError('Booking does not fit in user availability.')
        overlaps = Booking.objects.filter(
            user=self.context['user'],
            date=data['date'],
            start_time__lt=end_dt.time(),
            end_time__gt=data['start_time']
        )
        if self.instance:
            overlaps = overlaps.exclude(pk=self.instance.pk)
        if overlaps.exists():
            raise serializers.ValidationError('Booking overlaps with an existing booking.')
        return data
