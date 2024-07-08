from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class UserModelTests(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="test_user",
            email="test@test.com",
            password="test1234",
            first_name="first",
            last_name="last",
            role="admin"
        )

    def test_user_full_name(self):
        self.assertEqual(
            self.user.full_name,
            f"{self.user.first_name} {self.user.last_name}"
        )

    def test_user_str(self):
        self.assertEqual(
            str(self.user),
            f"{self.user.last_name} {self.user.first_name} - {self.user.role}"
        )
