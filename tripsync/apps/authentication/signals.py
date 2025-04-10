from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from apps.users.models import User
from apps.trips.models import Trip, TripParticipant

@receiver(post_save, sender=User)
def send_welcome_mail(sender, instance, created, **kwargs):
    if not created and instance.is_active:
        send_mail(
            subject="Welcome to TripSync!",
            message=f"Hi {instance.username}, thank you for verifying your email and joining TripSync!",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[instance.email],
            fail_silently=False,
        )

        # print("send_welcome_mail")


@receiver(post_save, sender = User)
def update_role_on_registration(sender, instance, created, **kwargs):
    if created:
        instance.role = "Viewer"
        instance.save()

# 

@receiver(post_save, sender= Trip)
def update_role_on_trip_creation(sender, instance, created, **kwargs):
    if created and instance.trip_organizer.role in ["Viewer","participant"] :
        instance.trip_organizer.role = "trip_admin"
        instance.trip_organizer.save()

@receiver(post_save, sender= Trip)
def update_role_on_participation(sender,instance,**kwargs):
    for participant in instance.participants.all():
        if participant.role != "trip_admin":
            participant.role = "participant"
            participant.save()


@receiver(post_save, sender=TripParticipant)
def update_user_role_on_participation(sender, instance, created, **kwargs):
    """Update the user's role to 'participant' when they join a trip as a participant."""
    if created and instance.user.role == 'viewer':
        instance.user.role = 'participant'
        instance.user.save() 