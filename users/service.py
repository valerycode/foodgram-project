from django.conf import settings
from django.core.mail import send_mail


def send(user_email):
    send_mail(
        'Тема',
        'Тело письма',
        settings.EMAIL_HOST_USER,
        [user_email],
        fail_silently=False
    )
