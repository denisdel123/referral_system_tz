from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from users.apps import UsersConfig
from . import views as users_views

app_name = UsersConfig.name
urlpatterns = [
    path('registration/', users_views.RegistrationUsers.as_view(), name='registration'),
    path('create-referral', users_views.CreateReferralCode.as_view(), name='create_referral'),
    path('profile/<id>', users_views.RetrieveUsers.as_view(), name='create_referral'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
