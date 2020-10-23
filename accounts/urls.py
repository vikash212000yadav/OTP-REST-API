from django.urls import path, include
from .views import *
from knox import views as knox_views

app_name = 'accounts'

urlpatterns = [
    path('validate_phone/', ValidatePhoneSendOTP.as_view()),
    path('validate_otp/', ValidateOTP.as_view()),
    path('register/', Register.as_view()),
    path('login/', LoginAPI.as_view()),
    path('logout/', knox_views.LogoutView.as_view()),
    path('attendee_register/', AttendeeRegister.as_view()),
]