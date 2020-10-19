from django.urls import path, include
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('validate_phone/', ValidatePhoneSendOTP.as_view()),
    path('validate_otp/', ValidateOTP.as_view()),
    path('register/', Register.as_view()),
]