from django.contrib import admin
from apps.trips.models import Trip, TripActivity,TripInvitation, TripItinerary, TripJoinRequest,TripParticipant
# Register your models here.
from guardian.admin import GuardedModelAdmin

admin.site.register(Trip)

class TripAdmin(GuardedModelAdmin):
    list_display = ('trip_organizer',)

admin.site.register(TripActivity)
admin.site.register(TripInvitation)
admin.site.register(TripItinerary)
admin.site.register(TripJoinRequest)
admin.site.register(TripParticipant)