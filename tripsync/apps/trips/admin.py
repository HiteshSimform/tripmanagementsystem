from django.contrib import admin
from apps.trips.models import Trip, TripActivity,TripInvitation, TripItinerary, TripJoinRequest,TripParticipant
# Register your models here.

admin.site.register(Trip)
admin.site.register(TripActivity)
admin.site.register(TripInvitation)
admin.site.register(TripItinerary)
admin.site.register(TripJoinRequest)
admin.site.register(TripParticipant)