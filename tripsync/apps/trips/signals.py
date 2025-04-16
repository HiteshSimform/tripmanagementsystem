from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TripParticipant, TripUserRelation, Trip


@receiver(post_save, sender=Trip)
def create_trip_user_relation(sender, instance, created, **kwargs):
    if created:
        user = instance.trip_organizer

        # trip = Trip.objects.get(id=trip)
        TripUserRelation.objects.get_or_create(
            trip_id=instance, user_id=user, defaults={"user_role": "trip_admin"}
        )
        print("Called")
        # if trip.trip_organizer == user:
        #     TripUserRelation.objects.get_or_create(
        #         trip_id=trip,
        #         user_id=user,
        #         defaults={'user_role': 'trip_admin'}
        #     )
        #     print("If Called")
        # else:
        #     TripUserRelation.objects.update_or_create(
        #         trip_id=trip,
        #         user_id=user,
        #         defaults={'user_role': 'participant'}
        #     )
        #     print("Else Called")
