from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
from core import constants


class ReferralCode(models.Model):
    name = models.CharField(max_length=constants.CHAR_LENGTH_REFERRAL, unique=True, verbose_name='Код')
    valid_until = models.DateTimeField(verbose_name='Дата окончания')

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        if not password:
            raise ValueError("Password is required")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser):

    email = models.EmailField(
        unique=True,
        verbose_name='Email'
    )
    first_name = models.CharField(
        max_length=constants.CHAR_LENGTH,
        **constants.NULLABLE
    )
    referral_code = models.ForeignKey(
        ReferralCode,
        on_delete=models.CASCADE,
        **constants.NULLABLE,
        verbose_name='Реферальный код'
    )
    invited_by = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        **constants.NULLABLE,
        related_name='users',
        verbose_name='Кто пригласил'
    )
    registration_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата регистрации'
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name='Модератор'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активен'
    )
    is_superuser = models.BooleanField(
        default=False,
        verbose_name='Администратор'
    )

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def clean(self):
        super().clean()
        if self.email:
            self.email = self.email.lower()

    def __str__(self):
        return self.first_name if self.first_name else self.email

