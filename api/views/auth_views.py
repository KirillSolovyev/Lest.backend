from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.throttling import UserRateThrottle
from django.shortcuts import get_object_or_404
from ..models import User, PhoneOTP
from ..serializers import UserSerializer
from ..common.errors import ErrorCode
import pyotp


class AuthView(APIView):
    throttle_scope = "authorization"

    def post(self, request):
        phone_number = request.data.get("phone_number")
        password = request.data.get("password")

        #TODO: implement error codes with description

        if phone_number is None or password is None:
            return Response({"error": ErrorCode.INCOMPLETE_DATA.value}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(phone_number=phone_number)
        if not user.exists():
            return Response({"error": ErrorCode.USER_NOT_REGISTERED.value}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(phone_number=phone_number, password=password)
        if not user:
            return Response({"error": ErrorCode.INVALID_CREDENTIALS.value}, status=status.HTTP_403_FORBIDDEN)

        token = get_object_or_404(Token, user=user)
        return Response({"token": token.key}, status=status.HTTP_200_OK)


class RegistrationView(APIView):
    throttle_scope = "registration"

    def put(self, request):
        phone = request.data.get("phone_number", False)
        phone_otp = PhoneOTP.objects.filter(phone_number__iexact=phone)
        if not phone_otp.exists() or not phone_otp.first().verified:
            return Response({"error": ErrorCode.PHONE_HAS_NO_VERIFY_REQUEST.value}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(phone_number__iexact=phone)
        if user.exists():
            return Response({"error": ErrorCode.USER_ALREADY_EXIST.value}, status=status.HTTP_400_BAD_REQUEST)

        serialized = UserSerializer(data=request.data)
        if serialized.is_valid():
            user = serialized.save()
            token = get_object_or_404(Token, user=user)
            return Response({"token": token.key}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": ErrorCode.INVALID_DATA.value}, status=status.HTTP_400_BAD_REQUEST)


class SendOTPThrottleMin(UserRateThrottle):
    scope = "send_otp_min"


class SendOTPThrottleMax(UserRateThrottle):
    scope = "send_otp_max"


class ConfirmOTPThrottle(UserRateThrottle):
    scope = "confirm_otp"


class ValidatePhoneOTPView(APIView):
    throttle_classes = []

    def get_throttles(self):
        if self.request.method.lower() == 'put':
            self.throttle_classes = [SendOTPThrottleMin, SendOTPThrottleMax]
        elif self.request.method.lower() == 'post':
            self.throttle_classes = [ConfirmOTPThrottle, ]
        return super(ValidatePhoneOTPView, self).get_throttles()

    def put(self, request):
        phone = request.data.get("phone_number", False)
        if phone:
            user = User.objects.filter(phone_number__iexact=phone)
            if user.exists():
                return Response({"error": ErrorCode.USER_ALREADY_EXIST.value}, status=status.HTTP_400_BAD_REQUEST)
            else:
                key = pyotp.random_base32()
                phone_otp = PhoneOTP.objects.filter(phone_number__iexact=phone)
                otp = pyotp.TOTP(key, interval=60)
                if phone_otp.exists():
                    phone_otp = phone_otp.first()
                    phone_otp.key = key
                    phone_otp.save()
                    print(otp.now())
                    return Response({"opt": otp.now()}, status=status.HTTP_200_OK)
                else:
                    phone_otp = PhoneOTP(phone_number=phone, key=key)
                    try:
                        phone_otp.full_clean()
                    except ValidationError:
                        return Response({"error": ErrorCode.INVALID_DATA.value}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        phone_otp.save()
                        print(otp.now())
                        return Response({"otp": otp.now()}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": ErrorCode.INCOMPLETE_DATA.value}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        phone = request.data.get("phone_number", False)
        otp = request.data.get("otp", False)
        if phone and otp:
            try:
                opt = int(otp)
            except:
                return Response({"error": ErrorCode.INVALID_DATA.value}, status=status.HTTP_400_BAD_REQUEST)
            phone_otp = PhoneOTP.objects.filter(phone_number__iexact=phone)
            if not phone_otp.exists():
                return Response({"error": ErrorCode.PHONE_HAS_NO_VERIFY_REQUEST.value}, status=status.HTTP_400_BAD_REQUEST)

            phone_otp = phone_otp.first()
            if phone_otp.verified:
                return Response({"error": ErrorCode.PHONE_ALREADY_VERIFIED.value}, status=status.HTTP_400_BAD_REQUEST)

            totp = pyotp.TOTP(phone_otp.key, interval=60)
            if not totp.verify(otp):
                return Response({"error": ErrorCode.INVALID_OTP.value}, status=status.HTTP_400_BAD_REQUEST)

            phone_otp.verified = True
            phone_otp.save()
            return Response({}, status=status.HTTP_200_OK)
        else:
            return Response({"error": ErrorCode.INCOMPLETE_DATA.value}, status=status.HTTP_400_BAD_REQUEST)
