from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TripParticipant, TripUserRelation, Trip


@receiver(post_save, sender=Trip)
def create_organizer_trip_relation(sender, instance, created, **kwargs):
    if created:
        TripUserRelation.objects.get_or_create(
            trip=instance,
            user=instance.trip_organizer,
            defaults={"user_role": "trip_admin"},
        )


@receiver(post_save, sender=TripParticipant)
def create_participant_trip_relation(sender, instance, created, **kwargs):
    if created:
        trip = instance.trip
        user = instance.user

        existing_relation = TripUserRelation.objects.filter(
            trip=trip, user=user
        ).first()

        if existing_relation:
            if existing_relation.user_role in ["trip_admin", "admin"]:
                return
            return
        TripUserRelation.objects.create(trip=trip, user=user, user_role="participant")
