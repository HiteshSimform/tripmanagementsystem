from celery import shared_task
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken


@shared_task
def delete_blacklisted_tokens():
    OutstandingToken.objects.filter(blacklistedtoken__isnull=False).delete()
