from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views


app_name = "main"   

urlpatterns = [
    path("", csrf_exempt(views.RegistrationView.as_view()), name="homepage"),
    path('validate-username', csrf_exempt(views.UsernameValidationView.as_view()), name="validate-username"),
    path("validate-lastname", csrf_exempt(views.LastnameValidationView.as_view()), name="validate-lastname"),
]