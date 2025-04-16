from rest_framework import serializers
from apps.trips.models import Trip, TripParticipant
from datetime import date


class TripSerializer(serializers.ModelSerializer):
    participants = serializers.SerializerMethodField()

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


class TripParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripParticipant
        fields = "__all__"
