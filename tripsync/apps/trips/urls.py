# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# # from apps.trips.views import TripViewSet,TripParticipantViewSet

# from

# # Create a router and register the viewsets
# router = DefaultRouter()
# router.register(r'trips', TripViewSet, basename='trip')
# router.register(r'trip-participants', TripParticipantViewSet)

# # URLs to be included in the project
# urlpatterns = [
#     path('', include(router.urls)),
# ]

from django.urls import path
from apps.trips.views import (
    TripListCreateView,
    TripDetailView,
    TripParticipantCreateView,
    TripParticipantDeleteView,
    TripParticipantListView,
    TripParticipantUpdateView,
    TripJoinRequestCreateView,
    TripJoinRequestActionView,
)

urlpatterns = [
    path("trips/", TripListCreateView.as_view(), name="trip-list-create"),
    path("trips/<int:pk>/", TripDetailView.as_view(), name="trip-detail"),
    path(
        "trips/<int:trip_id>/participants/",
        TripParticipantListView.as_view(),
        name="participant-list",
    ),
    path(
        "participants/", TripParticipantCreateView.as_view(), name="participant-create"
    ),
    path(
        "participants/<int:pk>/",
        TripParticipantUpdateView.as_view(),
        name="participant-update",
    ),
    path(
        "participants/<int:pk>/delete/",
        TripParticipantDeleteView.as_view(),
        name="participant-delete",
    ),
    path(
        "trip-join-request/",
        TripJoinRequestCreateView.as_view(),
        name="trip-join-request-create",
    ),
    path(
        "trip-join-request/<int:pk>/",
        TripJoinRequestActionView.as_view(),
        name="trip-join-request-action",
    ),
]
