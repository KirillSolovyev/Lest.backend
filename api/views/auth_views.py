from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.shortcuts import get_object_or_404


class AuthView(APIView):
    def post(self, request):
        phone_number = request.data.get("phone_number")
        password = request.data.get("password")

        #TODO: implement error codes with description

        if phone_number is None or password is None:
            return Response({"error": "incomplete_data"}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(phone_number=phone_number, password=password)
        if not user:
            return Response({"error": "invalid_credentials"}, status=status.HTTP_403_FORBIDDEN)

        token = get_object_or_404(Token, user=user)
        return Response({"token": token.key}, status=status.HTTP_200_OK)
