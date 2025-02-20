from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions
from . import serializers as users_serializers
from . import models as users_models


@extend_schema(
    summary="Регистрация пользователя.",
    description="Регистрация по почте и паролю так же можно использовать реферальный код",
)
class RegistrationUsers(generics.CreateAPIView):
    serializer_class = users_serializers.RegistrationUsersSerializer
    queryset = users_models.User.objects.all()



@extend_schema(
    summary="Создание реферального кода.",
    description="Создает реферальный код и добавляет его к пользователю.",
)
class CreateReferralCode(generics.CreateAPIView):
    serializer_class = users_serializers.CreateReferralCodeSerializer
    queryset = users_models.ReferralCode.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
