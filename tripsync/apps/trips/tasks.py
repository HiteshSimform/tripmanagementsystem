from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from datetime import datetime, timedelta, timezone
from apps.trips.models import TripParticipant, Trip
from django.conf import settings
from django.utils import timezone
@shared_task
def send_invitation_email(to_email, subject, body):
    send_mail(
        subject=subject,
        message=body,
        from_email="Chandreshkanzariya19123@gmail.com",
        recipient_list=[to_email],
    )
    return "Success"


from rest_framework_simplejwt.token_blacklist.models import (
    OutstandingToken,
    BlacklistedToken,
)


@shared_task
def delete_blacklisted_tokens():
    OutstandingToken.objects.filter(blacklistedtoken__isnull=False).delete()

@shared_task
def send_trip_reminder_email(trip_id):
    """
    Task to send reminder email to participants one day before the trip
    """
    trip = Trip.objects.get(id=trip_id)
    participants = TripParticipant.objects.filter(trip=trip)

    # reminder_time = trip.start_date - timedelta(days=1)
    now = timezone.now().date()
    reminder_date = trip.start_date - timedelta(days=1)

    # Only send emails to participants for the trips happening 1 day from now
    if now >= reminder_date:
    # if now == now:
        for participant in participants:
            # Render the email content using Jinja2 template
            subject = f"Reminder: Your Trip '{trip.trip_title}' Tomorrow"
            html_message = render_to_string(
                'emails/trip_reminder_email.html',  # Path to Jinja template
                {'user': participant.user, 'trip': trip}
            )

            send_mail(
                subject=subject,
                message='',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                html_message=html_message,  # Pass the rendered HTML email content
            )

    return f"Reminder emails sent for trip {trip_id}"