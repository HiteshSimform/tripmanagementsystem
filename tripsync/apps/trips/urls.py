from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.trips.views import (
    TripViewSet,
    TripInvitationViewSet,
    TripActivityViewSet,
    TripItineraryViewSet,
    TripJoinRequestViewSet,
    TripParticipantViewSet,
)

# Create a router and register the viewsets
router = DefaultRouter()
router.register(r'trips', TripViewSet, basename='trip')
router.register(r'trip-invitations', TripInvitationViewSet)
router.register(r'trip-activities', TripActivityViewSet)
router.register(r'trip-itineraries', TripItineraryViewSet)
router.register(r'trip-join-requests', TripJoinRequestViewSet)
router.register(r'trip-participants', TripParticipantViewSet)

# URLs to be included in the project
urlpatterns = [
    path('', include(router.urls)),
]