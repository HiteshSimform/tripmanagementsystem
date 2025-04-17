from django.core.mail import send_mail
from django.conf import settings


def send_join_request_notification(join_request):
    subject = f"{join_request.user.username} wants to join your trip: {join_request.trip.trip_title}"
    message = f"""
    Hey! {join_request.user.username} sent a request to join your trip.

    Message: {join_request.message}

    Approve: http://127.0.0.1:8000/trips/trip-join-request/{join_request.id}/?action=approve
    Reject: http://127.0.0.1:8000/trips/trip-join-request/{join_request.id}/?action=reject
    """
    organizer_email = join_request.trip.trip_organizer.email
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [organizer_email])
