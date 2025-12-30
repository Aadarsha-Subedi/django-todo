import random
from django.utils import timezone
from datetime import timedelta


def generate_otp():
    return random.randint(100000, 999999)

def otp_expiry():
    return timezone.now() + timedelta(minutes=10)


