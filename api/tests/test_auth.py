import json
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token
from ..common.errors import ErrorCode
from ..models import User
from ..serializers import UserSerializer


class AuthViewTest(APITestCase):
    phone_number = "+77055025601"
    password = "testPassword"

    def setUp(self):
        self.user = User.objects.create_user(phone_number=self.phone_number, password=self.password)
        self.url = reverse("login")

    def test_authentication(self):
        body = {"phone_number": self.phone_number, "password": self.password}
        response = self.client.post(self.url, json.dumps(body), content_type="application/json")
        token = Token.objects.get(user=self.user)
        self.assertIsNotNone(response.data.get("user"))
        self.assertEqual(response.data.get("token"), token.key)

    def test_invalid_credentials_auth(self):
        body = {"phone_number": self.phone_number, "password": "wrong_pass"}
        response = self.client.post(self.url, json.dumps(body), content_type="application/json")
        self.assertEqual(response.data.get("error"), ErrorCode.INVALID_CREDENTIALS.value)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_incomplete_data_auth(self):
        body = {"phone_number": self.phone_number}
        response = self.client.post(self.url, json.dumps(body), content_type="application/json")
        self.assertEqual(response.data.get("error"), ErrorCode.INCOMPLETE_DATA.value)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_such_user_auth(self):
        body = {"phone_number": "+12345", "password": "1233"}
        response = self.client.post(self.url, json.dumps(body), content_type="application/json")
        self.assertEqual(response.data.get("error"), ErrorCode.NO_SUCH_USER.value)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)