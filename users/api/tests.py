from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth.models import User
from rest_framework.serializers import ValidationError
from django.shortcuts import reverse
from model_bakery import baker
from faker import Faker


class TestPostList(APITestCase):
    """Testing Retrieving All Users list"""

    def setUp(self):
        self.client = APIClient()
        self.url = reverse("api_all_users")
        self.user = baker.make(User, _quantity=3)

    def test_post_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)


class TestCreateUser(APITestCase):
    """Testing Creating user with API"""

    def setUp(self):
        self.client = APIClient()
        self.url = reverse("api_create_user")
        self.faker = Faker()

    def test_create_user_invalied_password(self):
        username = self.faker.first_name()
        email = self.faker.email()
        password = "".join(self.faker.random_letters(length=4))
        response = self.client.post(
            self.url, {"username": username, "email": email, "password": password}
        )
        self.assertIn("Error", response.data)
        self.assertEqual(User.objects.count(), 0)

    def test_create_user(self):
        username = self.faker.first_name()
        email = self.faker.email()
        password = "".join(self.faker.random_letters(length=16))
        response = self.client.post(
            self.url, {"username": username, "email": email, "password": password}
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 1)
