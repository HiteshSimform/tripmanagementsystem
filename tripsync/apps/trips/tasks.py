from celery import shared_task
from django.core.mail import send_mail
from datetime import datetime, timedelta
@shared_task
def send_invitation_email(to_email, subject, body):
    send_mail(
        subject=subject,
        message=body,
        from_email='Chandreshkanzariya19123@gmail.com',
        recipient_list=[to_email]
    )
    return "Success"


from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
@shared_task
def delete_blacklisted_tokens():
    OutstandingToken.objects.filter(blacklistedtoken__isnull=False).delete()
# eta_time = datetime.now() + timedelta(minutes=1)
# delete_blacklisted_tokens.apply_async(eta=eta_time)