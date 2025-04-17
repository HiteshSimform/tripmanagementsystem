# from rest_framework import permissions
# from rest_framework.permissions import BasePermission
# from .models import TripUserRelation, TripJoinRequest


# class IsTripOrganizerOrReadOnly(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         return obj.trip_organizer == request.user


# class IsAdminOrTripParticipant(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return (
#             request.user.is_staff
#             or request.user == obj.trip_organizer
#             or request.user in obj.participants.all()
#         )


# class IsTripAdmin(BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return TripUserRelation.objects.filter(
#             user=request.user, trip=obj.trip, user_role="trip_admin"
#         ).exists()


# class IsTripParticipant(BasePermission):
#     def has_permission(self, request, view):
#         trip_id = view.kwargs.get("trip_id") or request.data.get("trip")
#         if not trip_id:
#             return False
#         return TripUserRelation.objects.filter(
#             trip_id=trip_id, user_id=request.user, user_role="participant"
#         ).exists()


# class IsTripAdminOrParticipant(BasePermission):
#     def has_permission(self, request, view):
#         trip_id = view.kwargs.get("trip_id") or request.data.get("trip")
#         if not trip_id:
#             return False
#         return TripUserRelation.objects.filter(
#             trip_id=trip_id,
#             user_id=request.user,
#             user_role__in=["trip_admin", "participant"],
#         ).exists()


# class IsTripOrganizer(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return obj.trip.trip_organizer == request.user or request.user.is_staff

from rest_framework import permissions
from rest_framework.permissions import BasePermission
from .models import TripUserRelation, TripJoinRequest


class IsTripOrganizerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read-only for anyone
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions only for the trip organizer
        return obj.trip_organizer == request.user


class IsAdminOrTripParticipant(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_staff
            or request.user == obj.trip_organizer
            or request.user in obj.participants.all()
        )


# class IsTripAdmin(BasePermission):
#     def has_permission(self, request, view):
#         trip_id = view.kwargs.get("trip_id") or request.data.get("trip")
#         if not trip_id:
#             return False
#         return TripUserRelation.objects.filter(
#             trip_id=trip_id, user_id=request.user, user_role="trip_admin"
#         ).exists()


class IsTripAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return TripUserRelation.objects.filter(
            user=request.user, trip=obj.trip, user_role="trip_admin"
        ).exists()


class IsTripParticipant(BasePermission):
    def has_permission(self, request, view):
        trip_id = view.kwargs.get("trip_id") or request.data.get("trip")
        if not trip_id:
            return False
        return TripUserRelation.objects.filter(
            trip_id=trip_id, user_id=request.user, user_role="participant"
        ).exists()


class IsTripAdminOrParticipant(BasePermission):
    def has_permission(self, request, view):
        trip_id = view.kwargs.get("trip_id") or request.data.get("trip")
        if not trip_id:
            return False
        return TripUserRelation.objects.filter(
            trip_id=trip_id,
            user_id=request.user,
            user_role__in=["trip_admin", "participant"],
        ).exists()


class IsTripOrganizer(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.trip.trip_organizer == request.user or request.user.is_staff
