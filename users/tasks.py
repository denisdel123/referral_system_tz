from celery import shared_task
from . import models as users_models


@shared_task()
def get_invited_by(invited_by_code):
    """Асинхронно ищем пользователя по реферальному коду"""
    return users_models.User.objects.filter(referral_code__name=invited_by_code).first()


@shared_task()
def create_user_task(email, password, invited_by_code):
    """Асинхронно создаем пользователя"""

    invited_by = users_models.User.objects.get(referral_code__name=invited_by_code) if invited_by_code else None

    user = users_models.User.objects.create_user(
        email=email,
        password=password,
        invited_by=invited_by
    )
    return user.id
