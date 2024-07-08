from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.management import call_command

from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()
REGISTER_USER_URL = reverse("user:register")
LOGIN_URL = reverse("user:login")
MANAGE_USER_URL = reverse("user:staff-list")


def detail_url(user_id):
    return reverse("user:staff-detail", args=[user_id])


class PublicUserApiTests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.data = {
            "username": "test_user",
            "password": "1234test"
        }
        self.user = User.objects.create_user(**self.data)

    def test_valid_user_login(self):
        res = self.client.post(LOGIN_URL, self.data)
        self.assertIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_invalid_user_login(self):
        invalid_data = {
            "username": "test_user",
            "password": "<wrong_password>"
        }

        res = self.client.post(LOGIN_URL, invalid_data)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class PrivateUserApiTests(TestCase):

    def setUp(self) -> None:
        call_command("create_groups")

        self.admin = User.objects.create_user(
            username="admin",
            password="test1234",
            role="admin"
        )
        self.manager = User.objects.create_user(
            username="manager",
            password="test1234",
            role="manager"
        )
        self.guard = User.objects.create_user(
            username="guard",
            password="test1234",
            role="guard"
        )
        self.sample_data = {
            "username": "test_user",
            "email": "user@user.com",
            "password": "1234%test",
            "first_name": "user_first_name",
            "last_name": "user_last_name",
            "role": "guard",
        }
        self.client = APIClient()

    def test_user_register_as_admin(self):
        self.client.force_authenticate(self.admin)

        res = self.client.post(REGISTER_USER_URL, self.sample_data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(**res.data)
        self.assertTrue(user.check_password(self.sample_data.get("password")))
        self.assertNotIn("password", res.data)

    def test_user_register_as_manager(self):
        self.client.force_authenticate(self.manager)

        res = self.client.post(REGISTER_USER_URL, self.sample_data)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_register_as_guard(self):
        self.client.force_authenticate(self.guard)

        res = self.client.post(REGISTER_USER_URL, self.sample_data)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_users_as_admin(self):
        self.client.force_authenticate(self.admin)
        res = self.client.get(MANAGE_USER_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 3)

    def test_list_users_as_non_admin(self):
        self.client.force_authenticate(self.manager)
        res = self.client.get(MANAGE_USER_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(self.guard)
        res = self.client.get(MANAGE_USER_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_user_as_any_role(self):
        self.client.force_authenticate(self.manager)
        url = detail_url(self.manager.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data.get("username"), self.manager.username)

    def test_update_user_as_admin(self):
        self.client.force_authenticate(self.admin)
        url = detail_url(self.guard.id)
        data = {"first_name": "new_first_name"}

        res = self.client.patch(url, data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.guard.refresh_from_db()
        self.assertEqual(self.guard.first_name, "new_first_name")

    def test_update_user_as_non_admin(self):
        self.client.force_authenticate(self.guard)
        url = detail_url(self.guard.id)
        data = {"first_name": "new_first_name"}

        res = self.client.patch(url, data)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
