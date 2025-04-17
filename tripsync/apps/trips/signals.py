# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import TripParticipant, TripUserRelation, Trip


# @receiver(post_save, sender=Trip)
# def create_trip_user_relation(sender, instance, created, **kwargs):
#     if created:
#         user = instance.trip_organizer

#         # trip = Trip.objects.get(id=trip)
#         TripUserRelation.objects.get_or_create(
#             trip_id=instance, user_id=user, defaults={"user_role": "trip_admin"}
#         )
#         print("Called")
#         # if trip.trip_organizer == user:
#         #     TripUserRelation.objects.get_or_create(
#         #         trip_id=trip,
#         #         user_id=user,
#         #         defaults={'user_role': 'trip_admin'}
#         #     )
#         #     print("If Called")
#         # else:
#         #     TripUserRelation.objects.update_or_create(
#         #         trip_id=trip,
#         #         user_id=user,
#         #         defaults={'user_role': 'participant'}
#         #     )
#         #     print("Else Called")


from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TripParticipant, TripUserRelation, Trip
 
@receiver(post_save, sender=Trip)
def create_organizer_trip_relation(sender, instance, created, **kwargs):
    """
    When a Trip is created, add the organizer as 'trip_admin' in TripUserRelation.
    """
    if created:
        TripUserRelation.objects.get_or_create(
            trip=instance,
            user=instance.trip_organizer,
            defaults={"user_role": "trip_admin"}
        )
 
 
@receiver(post_save, sender=TripParticipant)
def create_participant_trip_relation(sender, instance, created, **kwargs):
    """
    When a TripParticipant is added, ensure they are also added to TripUserRelation.
    Avoid duplicate or role downgrade if organizer joins own trip.
    """
    if created:
        trip = instance.trip
        user = instance.user
 
        existing_relation = TripUserRelation.objects.filter(trip=trip, user=user).first()
 
        if existing_relation:
            # If user is already a trip_admin or admin, do not change the role
            if existing_relation.user_role in ["trip_admin", "admin"]:
                return
            # If the relation exists but with a different role, don't change it
            return
 
        # If no relation exists, add as 'participant'
        TripUserRelation.objects.create(
            trip=trip,
            user=user,
            user_role="participant"
        )