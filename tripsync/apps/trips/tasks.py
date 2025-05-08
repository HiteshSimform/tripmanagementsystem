from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from datetime import datetime, timedelta, timezone
from apps.trips.models import TripParticipant, Trip
from django.conf import settings
from django.utils import timezone
from dotenv import load_dotenv
import os
load_dotenv()

@shared_task
def send_invitation_email(to_email, subject, body):
    send_mail(
        subject=subject,
        message=body,
        from_email=os.getenv("EMAIL_HOST_USER"),
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


# @shared_task
# def send_trip_reminder_email(trip_id):
#     """
#     Task to send reminder email to participants one day before the trip
#     """
#     trip = Trip.objects.get(id=trip_id)
#     participants = TripParticipant.objects.filter(trip=trip)
#     now = timezone.now().date()
#     reminder_date = trip.start_date - timedelta(days=1)

#     if now >= reminder_date:
#         # if now == now:
#         for participant in participants:
#             subject = f"Reminder: Your Trip '{trip.trip_title}' Tomorrow"
#             html_message = render_to_string(
#                 "emails/trip_reminder_email.html",
#                 {"user": participant.user, "trip": trip},
#             )

#             send_mail(
#                 subject=subject,
#                 message="",
#                 from_email=settings.DEFAULT_FROM_EMAIL,
#                 recipient_list=[settings.DEFAULT_FROM_EMAIL],
#                 html_message=html_message,
#             )

#     return f"Reminder emails sent for trip {trip_id}"


import logging
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from celery import shared_task
from trips.models import Trip, TripParticipant
from django.core.exceptions import ObjectDoesNotExist

logger = logging.getLogger(__name__)

@shared_task
def send_trip_reminder_email(trip_id):
    """
    Task to send reminder email to participants one day before the trip.
    Adds error handling and logging for better traceability.
    """
    try:
        trip = Trip.objects.get(id=trip_id)
    except ObjectDoesNotExist:
        logger.error(f"Trip with ID {trip_id} does not exist.")
        return f"Trip {trip_id} not found"

    reminder_date = trip.start_date - timedelta(days=1)
    today = timezone.now().date()

    if today >= reminder_date:
        participants = TripParticipant.objects.filter(trip=trip)
        if not participants.exists():
            logger.warning(f"No participants found for trip ID {trip_id}.")
            return f"No participants to notify for trip {trip_id}"

        for participant in participants:
            try:
                subject = f"Reminder: Your Trip '{trip.trip_title}' Tomorrow"
                html_message = render_to_string(
                    "emails/trip_reminder_email.html",
                    {"user": participant.user, "trip": trip},
                )
                send_mail(
                    subject=subject,
                    message="",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[participant.user.email],
                    html_message=html_message,
                )
                logger.info(f"Reminder email sent to {participant.user.email} for trip {trip_id}.")
            except Exception as e:
                logger.exception(f"Failed to send reminder to {participant.user.email}: {e}")

        return f"Reminder emails processed for trip {trip_id}"

    logger.info(f"Reminder not sent; current date {today} is before reminder date {reminder_date}.")
    return f"No reminders sent; too early for trip {trip_id}"
