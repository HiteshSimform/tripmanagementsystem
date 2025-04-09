from django.db import models
from apps.users.models import User
# Create your models here.
from django.conf import settings
from django.utils import timezone
import uuid

# User = settings.AUTH_USER_MODEL

class Trip(models.Model):
    VISIBILITY_CHOICES = [
        ('private','Private'),
        ('public','Public'),
    ]

    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    trip_organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_trip')
    trip_title = models.CharField(max_length=255)
    trip_description = models.TextField(blank=True)
    trip_destination = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    trip_visibility = models.CharField(max_length=10,choices=VISIBILITY_CHOICES, default='private')
    trip_image = models.ImageField(upload_to='trip_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.title} ({self.trip_organizer})"
    
class TripParticipant(models.Model):
    ROLE_CHOICES = [
        ('participant','Participant'),
        ('coorganizer','Co-Organizer'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='participants')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='participant')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('trip', 'user')
    
    def __str__(self):
        return f"{self.user} in {self.trip} as {self.role}"
    

class TripItinerary(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='itineraries')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date = models.DateField()

    def __str__(self):
        return f"Itinerary: {self.title} on {self.date}"
    

class TripActivity(models.Model):
    itinerary = models.ForeignKey(TripItinerary, on_delete=models.CASCADE,related_name='activities')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Trip Activity : {self.title} at {self.start_time}"
    

class TripJoinRequest(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='trip_join_requests')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=[('pending','Pending'),('approved','Approved'),('rejected','Rejected')],default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('trip', 'user')

    def __str__(self):
        return f"TripJoinRequest: {self.user}, to {self.trip} ({self.status})"
    
class TripInvitation(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='invitations')
    email = models.EmailField()
    invited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    status = models.CharField(max_length=10, choices=[('pending','Pending'),('accepted','Accepted'),('expired','Expired')], default='pending')
    invited_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField()

    def is_expired(self):
        return timezone.now() > self.expired_at
    
    def __str__(self):
        return f"Invited to {self.mail} for {self.trip} ({self.status})"
    
