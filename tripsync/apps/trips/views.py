from rest_framework.response import Response
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView,
    DestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from apps.trips.permissions import (
    IsTripOrganizerOrReadOnly,
    IsTripAdmin,
    IsTripOrganizer,
)
from apps.trips.serializers import (
    TripSerializer,
    TripParticipantSerializer,
    TripJoinRequestActionSerializer,
    TripJoinRequestSerializer,
    TripPublicPreviewSerializer,
)
from apps.trips.models import Trip, TripParticipant, TripUserRelation, TripJoinRequest
from django.db.models import Q
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework import status, generics, permissions, serializers
from .emails import send_join_request_notification
from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from uuid import UUID
from django.core.mail import send_mail


class TripListCreateView(ListCreateAPIView):
    serializer_class = TripSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Trip.objects.filter(
            Q(trip_visibility="public")
            | Q(trip_organizer=user)
            | Q(participants__user=user)
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(trip_organizer=self.request.user)


class TripDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    permission_classes = [IsAuthenticated, IsTripOrganizerOrReadOnly]


class TripParticipantCreateView(CreateAPIView):
    queryset = TripParticipant.objects.all()
    serializer_class = TripParticipantSerializer
    permission_classes = [IsAuthenticated]


class TripParticipantListView(ListAPIView):
    serializer_class = TripParticipantSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        trip_id = self.kwargs.get("trip_id")
        return TripParticipant.objects.filter(trip_id=trip_id)


class TripParticipantUpdateView(RetrieveUpdateAPIView):
    queryset = TripParticipant.objects.all()
    serializer_class = TripParticipantSerializer
    permission_classes = [IsAuthenticated]


class TripParticipantDeleteView(DestroyAPIView):
    queryset = TripParticipant.objects.all()
    serializer_class = TripParticipantSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            {"message": "Trip participant deleted successfully!"},
            status=status.HTTP_200_OK,
        )


class TripJoinRequestCreateView(generics.CreateAPIView):
    queryset = TripJoinRequest.objects.all()
    serializer_class = TripJoinRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        trip_id = self.request.data.get("trip_id")
        trip_instance = get_object_or_404(Trip, id=trip_id)

        if not trip_instance.trip_visibility == "public":
            raise serializers.ValidationError("This trip is not public.")

        if TripJoinRequest.objects.filter(
            trip=trip_instance, user=self.request.user
        ).exists():
            raise serializers.ValidationError(
                "You have already requested to join this trip."
            )
        join_request = serializer.save(trip=trip_instance, user=self.request.user)
        join_request.full_clean()
        send_join_request_notification(join_request)


class TripJoinRequestActionView(generics.UpdateAPIView):
    queryset = TripJoinRequest.objects.all()
    serializer_class = TripJoinRequestActionSerializer
    permission_classes = [IsAuthenticated, IsTripOrganizer]

    def get_queryset(self):
        return TripJoinRequest.objects.filter(status="pending")


class TripJoinRequestDetailView(generics.UpdateAPIView):
    queryset = TripJoinRequest.objects.all()
    serializer_class = TripJoinRequestActionSerializer
    permission_classes = [permissions.IsAuthenticated, IsTripOrganizer]


class CancelJoinRequestAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTripAdmin]

    def delete(self, request, request_id):
        join_request = get_object_or_404(TripJoinRequest, id=request_id)

        if join_request.user != request.user:
            return Response(
                {"detail": "Not allowed to cancel this request."}, status=403
            )

        if join_request.status != "pending":
            return Response(
                {"detail": "Only pending requests can be canceled."}, status=400
            )

        join_request.delete()
        return Response({"detail": "Join request canceled."}, status=204)


class TripPreviewAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        trip = Trip.objects.filter(id=pk, trip_visibility="public").first()
        if not trip:
            return Response({"detail": "Trip not found or is not public."}, status=404)
        serializer = TripPublicPreviewSerializer(trip)
        return Response(serializer.data)
