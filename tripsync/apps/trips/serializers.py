from rest_framework import serializers
from apps.trips.models import Trip, TripActivity, TripInvitation, TripItinerary, TripJoinRequest, TripParticipant

class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip 
        fields = "__all__"

class TripActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = TripActivity
        fields = "__all__"

class TripInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripInvitation
        fields = "__all__"

class TripItinerarySerializer(serializers.ModelSerializer):
    class Meta:
        model = TripItinerary
        fields = "__all__"

class TripJoinRequestSerializer(serializers.Serializer):
    class Meta:
        model = TripJoinRequest
        fields = "__all__"

class TripParticipantSerializer(serializers.Serializer):
    class Meta:
        model = TripParticipant
        fields = "__all__"