from django.urls import path

from users.apps import UsersConfig
from . import views as users_views

app_name = UsersConfig.name
urlpatterns = [
    path('registration', users_views.RegistrationUsers.as_view(), name='registration')
]