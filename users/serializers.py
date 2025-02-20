import datetime
from datetime import timedelta

from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from rest_framework import serializers
from . import models as users_models
from . import tasks as users_tasks


class RegistrationUsersSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True
    )
    invited_by = serializers.CharField(
        write_only=True,
        required=False
    )

    class Meta:
        model = users_models.User
        fields = ["email", "password1", 'password2', "invited_by"]

    def validate(self, attrs):
        if attrs["password1"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Пароль не совпадает"})
        return attrs

    def create(self, validated_data):
        invited_by_code = validated_data.pop("invited_by", None)
        invited_by = None
        if invited_by_code:
            invited_by = users_models.User.objects.filter(
                referral_code__name=invited_by_code
            ).first()
        user = users_models.User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password1"],
            invited_by=invited_by
        )
        return user


class CreateReferralCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = users_models.ReferralCode
        fields = ["name", "valid_until"]

    def validate(self, attrs):
        data_now = timezone.now()
        if attrs['valid_until'] <= data_now:
            raise serializers.ValidationError({"data": "Дата должна быть в будущем"})
        if not attrs['name'].isupper():
            raise serializers.ValidationError({"name": "Код должен содержать только заглавные буквы"})

        return attrs

    def create(self, validated_data):
        user = self.context["request"].user

        users_models.ReferralCode.objects.filter(owner=user).delete()

        create_referral = users_models.ReferralCode.objects.create(
            name=validated_data["name"],
            valid_until=validated_data["valid_until"]
        )

        user.referral_code = create_referral
        user.save()

        return create_referral
