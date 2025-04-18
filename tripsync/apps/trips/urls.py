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
    TripPreviewAPIView,
    CancelJoinRequestAPIView,
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
    path(
        "trips/preview/<int:pk>/",
        TripPreviewAPIView.as_view(),
        name="trip-public-preview",
    ),
    path(
        "trips/join-request/<int:request_id>/cancel/",
        CancelJoinRequestAPIView.as_view(),
        name="cancel-join-request",
    ),
]
