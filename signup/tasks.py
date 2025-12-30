from celery import shared_task

from django.core.mail import EmailMessage, get_connection
from django.conf import settings
from django.utils import timezone

from .models import OTP

@shared_task(bind=True,
             autoretry_for=(Exception, ),
             retry_backoff=5,
             retry_kwargs={'max_retries': 3})
def send_signup_verification_email(self, to_mail, otp):
    with get_connection(host=settings.EMAIL_HOST,
                        port=settings.EMAIL_PORT,
                        username=settings.EMAIL_HOST_USER,
                        password=settings.EMAIL_HOST_PASSWORD,
                        use_tls=settings.EMAIL_USE_TLS) as connection:
        subject = "Welcome to Aadarsha's Backend System."
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [
            to_mail,
        ]
        message = f'This is an auto generated message. Please verify your email with the otp: {otp}'
        EmailMessage(subject,
                     message,
                     email_from,
                     recipient_list,
                     connection=connection).send()

@shared_task(bind=True, autoretry_for=(Exception, ),)
def clear_expired_otp_records(self):
    now = timezone.now()
    deleted_count, details = OTP.objects.filter(expires_at__lt=now).delete()
    return deleted_count
