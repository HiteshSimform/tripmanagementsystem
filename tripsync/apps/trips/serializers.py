from rest_framework import serializers
from apps.trips.models import Trip, TripParticipant, TripJoinRequest, TripUserRelation
from datetime import date
from apps.users.serializers import UserSerializer


class TripSerializer(serializers.ModelSerializer):
    participants = serializers.SerializerMethodField()
    total_participants = serializers.SerializerMethodField()
    class Meta:
        model = Trip
        # fields = "__all__"
        fields = [
            "id",
            "participants",
            "trip_title",
            "trip_description",
            "trip_destination",
            "start_date",
            "end_date",
            "trip_visibility",
            "trip_image",
            "created_at",
            "updated_at",
            "trip_organizer",
            "total_participants",
        ]
        read_only_fields = ["trip_organizer", "created_at", "updated_at"]

    def get_participants(self, obj):
        user = self.context["request"].user
        # organizer_email = obj.trip_organizer.email
        trip_name = obj.trip_title

        # Check if user is organizer or a participant
        if (
            user == obj.trip_organizer
            or TripParticipant.objects.filter(user=user, trip=obj).exists()
        ):
            # Use the TripParticipant relation
            return [
                f"{participant.user.username} in ({trip_name})"
                for participant in obj.participants.all()
            ]
        return None

    def validate(self, data):
        start_date = data.get(
            "start_date", self.instance.start_date if self.instance else None
        )
        end_date = data.get(
            "end_date", self.instance.end_date if self.instance else None
        )

        if start_date and start_date < date.today():
            raise serializers.ValidationError(
                "Start date must be today or a future date."
            )

        if start_date and end_date and end_date < start_date:
            raise serializers.ValidationError("End date must be after start date.")
        return data
    
    # Store Procedure
    def get_total_participants(self, obj):
        from apps.trips.utils import get_total_trip_participants
        return get_total_trip_participants(obj.id)


class TripParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripParticipant
        fields = "__all__"


class TripJoinRequestSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    trip = TripSerializer(read_only=True)
    trip_id = serializers.PrimaryKeyRelatedField(
        queryset=Trip.objects.all(), write_only=True, source="trip"
    )

    class Meta:
        model = TripJoinRequest
        fields = ["id", "trip", "trip_id", "user", "message", "status", "created_at"]
        read_only_fields = ["status", "created_at"]

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user
        trip = validated_data["trip"]

        # Prevent duplicate join request manually (as safety net)
        if TripJoinRequest.objects.filter(user=user, trip=trip).exists():
            raise serializers.ValidationError(
                "You have already requested to join this trip."
            )

        return TripJoinRequest.objects.create(user=user, **validated_data)


class TripJoinRequestActionSerializer(serializers.ModelSerializer):
    action = serializers.ChoiceField(choices=["approve", "reject"], write_only=True)

    class Meta:
        model = TripJoinRequest
        fields = ["id", "status", "action"]

    def update(self, instance, validated_data):
        action = validated_data.get("action")

        if instance.status != "pending":
            raise serializers.ValidationError(
                "This request has already been processed."
            )

        if action == "approve":
            instance.status = "approved"

            # Add to TripParticipant
            TripParticipant.objects.get_or_create(
                user=instance.user, trip=instance.trip
            )

            # Also add to TripUserRelation with role 'participant'
            TripUserRelation.objects.get_or_create(
                user=instance.user,
                trip_id=instance.trip,
                defaults={"user_role": "participant"},
            )

        elif action == "reject":
            instance.status = "rejected"

        instance.save()
        return instance
