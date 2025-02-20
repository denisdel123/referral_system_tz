from celery import shared_task
from django.core.mail import send_mail

from config import settings
from . import models as users_models


# @shared_task()
# def get_invited_by(invited_by_code):
#     """Асинхронно ищем пользователя по реферальному коду"""
#     return users_models.User.objects.filter(referral_code__name=invited_by_code).first()
#
#
# @shared_task()
# def create_user_task(email, password, invited_by_code):
#     """Асинхронно создаем пользователя"""
#
#     invited_by = users_models.User.objects.get(referral_code__name=invited_by_code) if invited_by_code else None
#
#     user = users_models.User.objects.create_user(
#         email=email,
#         password=password,
#         invited_by=invited_by
#     )
#     return user.id

@shared_task
def get_invited_by(invited_by_code):
    """Асинхронно ищем пользователя по реферальному коду"""
    return users_models.User.objects.filter(referral_code__name=invited_by_code).values_list("id", flat=True).first()


@shared_task
def create_user_task(email, password, invited_by_id):
    """Асинхронно создаем пользователя"""
    invited_by = users_models.User.objects.get(id=invited_by_id) if invited_by_id else None
    user = users_models.User.objects.create_user(email=email, password=password, invited_by=invited_by)
    return user.id  # Возвращаем ID созданного пользователя


@shared_task
def send_welcome_email(email_to, code, email_from=None):
    email_from = email_from or settings.DEFAULT_FROM_EMAIL
    send_mail(
        "Реферальный код!",
        f"Здравствуйте! Ваш реферальный код: {code}",
        from_email=email_from,
        recipient_list=[email_to],
        fail_silently=False,
    )
