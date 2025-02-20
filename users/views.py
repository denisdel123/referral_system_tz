from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers as users_serializers
from . import models as users_models
from . import tasks as users_tasks


@extend_schema(
    summary="Регистрация пользователя.",
    description="Регистрация по почте и паролю так же можно использовать реферальный код",
)
class RegistrationUsers(generics.CreateAPIView):
    serializer_class = users_serializers.RegistrationUsersSerializer
    queryset = users_models.User.objects.all()


@extend_schema(
    summary="Профиль пользователей.",
    description="При передачи id пользователя можно посмотреть все информацию об этом пользователе",
)
class RetrieveUsers(generics.RetrieveAPIView):
    queryset = users_models.User.objects.all()
    serializer_class = users_serializers.RetrieveUsersSerializer
    lookup_field = "id"


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


@extend_schema(
    summary="Удаление реферального кода.",
    description="Реферальный код автоматически удаляется при использовании.",
)
class DestroyReferralCode(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = request.user

        if not user.referral_code:
            return Response({"error": "У вас нет реферального кода"}, status=status.HTTP_400_BAD_REQUEST)

        # Удаляем код
        user.referral_code.delete()
        user.referral_code = None
        user.save()

        return Response({"message": "Реферальный код удален"}, status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    summary="Получить реферальный код по email.",
    description="При вводе email пользователя существующего в базе, приходит его реферальный код если он есть.",
)
class GetReferralCodeByEmailView(APIView):
    serializer_class = users_serializers.GetReferralCodeSerializer  # Добавляем это

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = users_serializers.GetReferralCodeSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]

            try:
                user = users_models.User.objects.get(email=email)
            except users_models.User.DoesNotExist:
                return Response({"error": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)

            if not user.referral_code:
                return Response({"error": "У пользователя нет реферального кода"}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"referral_code": user.referral_code.name}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
