from django.contrib import admin
from apps.trips.models import Trip, TripParticipant

# Register your models here.

admin.site.register(Trip)
admin.site.register(TripParticipant)
