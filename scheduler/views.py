from django.shortcuts import render

from rest_framework import generics, permissions
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import APIToken

class APITokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION', '')
        if auth.startswith('Bearer '):
            token = auth.split(' ', 1)[1]
            try:
                api_token = APIToken.objects.select_related('user').get(key=token)
                return (api_token.user, None)
            except APIToken.DoesNotExist:
                pass
        raise AuthenticationFailed('Invalid or missing API token.')
from .models import WeeklyAvailability, Booking
from .serializers import WeeklyAvailabilitySerializer, BookingSerializer
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status

class WeeklyAvailabilityListCreateView(generics.ListCreateAPIView):
    serializer_class = WeeklyAvailabilitySerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = [APITokenAuthentication]

    def get_queryset(self):
        user = self.request.user
        return WeeklyAvailability.objects.filter(user=user)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

class BookingListCreateView(generics.ListCreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = [APITokenAuthentication]

    def get_queryset(self):
        # Always return bookings for the authenticated user
        user = self.request.user
        return Booking.objects.filter(user=user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
