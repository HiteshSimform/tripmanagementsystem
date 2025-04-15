from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from apps.users.models import User
from apps.trips.models import Trip, TripParticipant, TripUserRelation

# @receiver(post_save, sender=User)
# def send_welcome_mail(sender, instance, created, **kwargs):
#     if not created and instance.is_active:
#         send_mail(
#             subject="Welcome to TripSync!",
#             message=f"Hi {instance.username}, thank you for verifying your email and joining TripSync!",
#             from_email=settings.EMAIL_HOST_USER,
#             recipient_list=[instance.email],
#             fail_silently=False,
#         )

#         # print("send_welcome_mail")

@receiver(pre_save, sender=User)
def cache_user_activation_status(sender, instance, **kwargs):
    try:
        old_instance = User.objects.get(pk=instance.pk)
        instance._was_inactive = not old_instance.is_active and instance.is_active
    except User.DoesNotExist:
        instance._was_inactive = False

@receiver(post_save, sender=User)
def send_welcome_mail(sender, instance, created, **kwargs):
    if not created and hasattr(instance, "_was_inactive") and instance._was_inactive:
        print(">>> Sending welcome email to:", instance.email)

        send_mail(
            subject="Welcome to TripSync!",
            message=f"Hi {instance.username}, thank you for verifying your email and joining TripSync!",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[instance.email],
            fail_silently=False,
        )


@receiver(post_save, sender = User)
def update_role_on_registration(sender, instance, created, **kwargs):
    if created:
        instance.role = "viewer"
        instance.save()

# 

@receiver(post_save, sender= Trip)
def update_role_on_trip_creation(sender, instance, created, **kwargs):
    if created:
        # instance.trip_organizer.role = "trip_admin"
        # instance.trip_organizer.save()
        trip_user_relation = TripUserRelation(
            trip_id=instance,
            user_id=instance.trip_organizer,
            user_role='trip_admin'
        )
        trip_user_relation.save()

# @receiver(post_save, sender= Trip)
# def update_role_on_participation(sender,instance,**kwargs):
#     for participant in instance.participants.all():
#         if participant.role != "trip_admin":
#             participant.role = "participant"
#             participant.save()


@receiver(post_save, sender=TripParticipant)
def update_trip_admin_to_participant(sender, instance, created, **kwargs):
    if created:
        user_roles_in_other_trips = instance.user.tripuserrelation_set.filter(user_role='trip_admin').exists()
        if user_roles_in_other_trips and instance.role == 'participant':
            instance.role = 'participant'  
            instance.save()

@receiver(post_save, sender=TripParticipant)
def update_user_role_on_participation(sender, instance, created, **kwargs):
    """Update the user's role to 'participant' when they join a trip as a participant."""
    if created and instance.user.role == 'viewer':
        instance.user.role = 'participant'
        instance.user.save() 