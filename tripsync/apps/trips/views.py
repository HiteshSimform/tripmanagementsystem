from django.shortcuts import render
from apps.trips.serializers import TripActivitySerializer,TripInvitationSerializer,TripItinerarySerializer,TripJoinRequestSerializer,TripParticipantSerializer,TripSerializer
from apps.trips.models import Trip,TripInvitation,TripActivity,TripItinerary,TripJoinRequest,TripParticipant
from django.views import View
from rest_framework import viewsets, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

# Create your views here.

class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    permission_classes = [IsAuthenticated]

class TripInvitationViewSet(viewsets.ModelViewSet):
    queryset = TripInvitation.objects.all()
    serializer_class = TripInvitationSerializer
    permission_classes = [IsAuthenticated]

class TripActivityViewSet(viewsets.ModelViewSet):
    queryset = TripActivity.objects.all()
    serializer_class = TripActivitySerializer
    permission_classes = [IsAuthenticated]

class TripItineraryViewSet(viewsets.ModelViewSet):
    queryset = TripItinerary.objects.all()
    serializer_class = TripItinerary
    permission_classes = [IsAuthenticated]

class TripJoinRequestViewSet(viewsets.ModelViewSet):
    queryset = TripJoinRequest.objects.all()
    serializer_class = TripJoinRequest
    permission_classes = [IsAuthenticated]

class TripParticipantViewSet(viewsets.ModelViewSet):
    queryset = TripParticipant.objects.all()
    serializer_class = TripParticipant
    permission_classes = [IsAuthenticated]