from django.contrib.auth import get_user_model
from django.test import TestCase


class UserModelTests(TestCase):
    def setUp(self) -> None:
        self.email = "test@email.com"
        self.password = "testpasswd"

    def test_create_regular_user(self):
        user = get_user_model().objects.create_user(
            email=self.email,
            password=self.password
        )

        self.assertEqual(self.email, user.email)
        self.assertTrue(self.password, user.check_password(self.password))
        self.assertEqual(user.is_staff, False)

    def test_create_admin(self):
        admin = get_user_model().objects.create_superuser(
            email=self.email,
            password=self.password
        )

        self.assertEqual(self.email, admin.email)
        self.assertTrue(self.password, admin.check_password(self.password))
        self.assertEqual(admin.is_staff, True)
        self.assertEqual(admin.is_superuser, True)
