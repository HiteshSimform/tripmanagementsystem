from django.db import models
from apps.users.models import User

# Create your models here.
from django.conf import settings
from django.utils import timezone
import uuid
from datetime import date, datetime
from django.core.exceptions import ValidationError


class Trip(models.Model):
    VISIBILITY_CHOICES = [
        ("private", "Private"),
        ("public", "Public"),
    ]
    trip_organizer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="organized_trip"
    )
    trip_title = models.CharField(max_length=255)
    trip_description = models.TextField(blank=True)
    trip_destination = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    trip_visibility = models.CharField(
        max_length=10, choices=VISIBILITY_CHOICES, default="private"
    )
    trip_image = models.ImageField(upload_to="trip_images/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    trip_participants = models.ManyToManyField(
        User, related_name="joined_trips", blank=True
    )

    def clean(self):
        if self.end_date < self.start_date:
            raise ValidationError(
                "End Date is always greater than Start Date, So enter Valid date"
            )

        if self.start_date < date.today():
            raise ValidationError("Start date must be today or any future date")

    def __str__(self):
        return f"{self.trip_title} ({self.trip_organizer})"


class TripParticipant(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trip = models.ForeignKey(
        Trip, on_delete=models.CASCADE, related_name="participants"
    )
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("trip", "user")

    def clean(self):
        if (
            self.trip.trip_visibility == "private"
            and self.user != self.trip.trip_organizer
        ):
            raise ValidationError("This trip for only organizers")

    def __str__(self):
        return f"{self.user} in {self.trip}"


class TripUserRelation(models.Model):
    ROLE_CHOICE = [
        ("admin", "Admin"),
        ("trip_admin", "Trip Admin"),
        ("participant", "Trip Participant"),
        ("viewer", "Viewer"),
        ("guest", "Guest"),
    ]
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_role = models.CharField(max_length=20, choices=ROLE_CHOICE, default="guest")


class TripJoinRequest(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    trip = models.ForeignKey(
        "Trip", on_delete=models.CASCADE, related_name="trip_join_requests"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("trip", "user")  # Prevent duplicate join requests

    def clean(self):
        # Prevent join request to private trips if user is neither organizer nor participant
        from .models import TripUserRelation

        if self.trip.trip_visibility == "private":
            is_member = TripUserRelation.objects.filter(
                trip=self.trip, user=self.user
            ).exists()

            if not is_member:
                raise ValidationError(
                    "You can't request to join a private trip you're not a part of."
                )

    def __str__(self):
        return f"JoinRequest: {self.user.username} → {self.trip.trip_title} [{self.status}]"
