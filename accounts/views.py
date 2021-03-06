import random
from django.contrib.auth import login
from django.shortcuts import render
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User, PhoneOTP
from django.shortcuts import get_object_or_404
from .serializer import *
from knox.views import LoginView as KnoxLoginView
from knox.auth import TokenAuthentication


# Create your views here.


class ValidatePhoneSendOTP(APIView):
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone')
        if phone_number:
            phone = str(phone_number)
            user = User.objects.filter(phone__iexact=phone)
            if user.exists():
                return Response({
                    'status': False,
                    'detail': 'Phone number already exist'
                })
            else:
                key = send_otp(phone)
                if key:
                    old = PhoneOTP.objects.filter(phone__iexact=phone)
                    if old.exists():
                        old = old.first()
                        count = old.count
                        if count > 10:
                            return Response({
                                'status': False,
                                'detail': 'Sending OTP Error. Limit exceeded. Please contact customer support'
                            })
                        old.count = count + 1
                        old.save()
                        print("Count increase", count)
                        return Response({
                            'status': True,
                            'detail': 'OTP sent Successfully'
                        })
                    else:
                        PhoneOTP.objects.create(
                            phone=phone,
                            otp=key,
                        )
                        return Response({
                            'status': True,
                            'detail': 'OTP sent Successfully'
                        })
                else:
                    return Response({
                        'status': False,
                        'detail': 'Sending OTP Error'
                    })
        else:
            return Response({
                'status': False,
                'detail': 'Phone number is not given in post request'
            })


def send_otp(phone):
    if phone:
        key = random.randint(999, 9999)
        # link = f"https://2factor.in/API/R1/?module=TRANS_SMS&apikey=75547813-11e2-11eb-9fa5-0200cd936042&to={phone}&from=NuNorm&templatename=NuNorm&var1={phone}&var2={key}"
        print(key)
        return key

    else:
        return False


class ValidateOTP(APIView):
    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', False)
        otp_sent = request.data.get('otp', False)

        if phone and otp_sent:
            old = PhoneOTP.objects.filter(phone__iexact=phone)
            if old.exists():
                old = old.first()
                otp = old.otp
                if str(otp_sent) == str(otp):
                    old.validated = True
                    old.save()
                    return Response({
                        'status': True,
                        'detail': 'OTP MAtched. Please proceed for registration.'
                    })
                else:
                    return Response({
                        'status': False,
                        'detail': 'OTP Incorrect!'
                    })
            else:
                return Response({
                    'status': False,
                    'detail': 'First proceed via sending otp request'
                })
        else:
            return Response({
                'status': False,
                'detail': 'Please provide both phone and otp for validation.'
            })


class Register(APIView):
    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', False)
        password = request.data.get('password', False)

        if phone and password:
            old = PhoneOTP.objects.filter(phone__iexact=phone)
            if old.exists():
                old = old.first()
                validated = old.validated
                if validated:
                    temp_data = {
                        'phone': phone,
                        'password': password
                    }
                    serializer = CreateUserSerializer(data=temp_data)
                    serializer.is_valid(raise_exception=True)
                    user = serializer.save()
                    old.delete()
                    return Response({
                        'status': True,
                        'detail': 'Account created'
                    })
                else:
                    return Response({
                        'status': False,
                        'detail': "OTP haven't verified. First do that step."
                    })
            else:
                return Response({
                    'status': False,
                    'detail': 'Please verify phone first'
                })
        else:
            return Response({
                'status': False,
                'detail': 'Both phone and password are not sent'
            })


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super().post(request, format=None)


class AttendeeRegister(APIView):
    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', False)
        password = request.data.get('password', False)

        if phone and password:
            old = PhoneOTP.objects.filter(phone__iexact=phone)
            if old.exists():
                old = old.first()
                validated = old.validated
                if validated:
                    temp_data = {
                        'phone': phone,
                        'password': password
                    }
                    serializer = AttendeeSerializer(data=temp_data)
                    serializer.is_valid(raise_exception=True)
                    user = serializer.save()
                    old.delete()
                    return Response({
                        'status': True,
                        'detail': 'Account created'
                    })
                else:
                    return Response({
                        'status': False,
                        'detail': "OTP haven't verified. First do that step."
                    })
            else:
                return Response({
                    'status': False,
                    'detail': 'Please verify phone first'
                })
        else:
            return Response({
                'status': False,
                'detail': 'Both phone and password are not sent'
            })
