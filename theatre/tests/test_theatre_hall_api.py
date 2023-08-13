from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from theatre.models import TheatreHall
from theatre.serializers import TheatreHallSerializer


THEATRE_HALL_URL = reverse("theatre:theatrehall-list")


def sample_theatre_hall(**params):
    defaults = {"name": "Test hall", "rows": 15, "seats_in_row": 20}
    defaults.update(params)

    return TheatreHall.objects.create(**defaults)


class UnauthenticatedTheatreHallsApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(THEATRE_HALL_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedTheatreHallsApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpassword",
        )
        self.client.force_authenticate(self.user)

    def test_theatre_hall_list_user_access(self):
        sample_theatre_hall(name="Test hall1", rows=15, seats_in_row=20)
        sample_theatre_hall(name="Test hall2", rows=10, seats_in_row=15)

        response = self.client.get(THEATRE_HALL_URL)

        theatre_halls = TheatreHall.objects.all()
        serializer = TheatreHallSerializer(theatre_halls, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_theatre_hall_forbidden(self):
        payload = {
            "first_name": "first",
            "last_name": "last"

        }
        response = self.client.post(THEATRE_HALL_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminTheatreHallApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            "admin@test.com",
            "testpassword",
        )
        self.client.force_authenticate(self.user)

    def test_theatre_hall_list_admin_access(self):
        sample_theatre_hall(name="Test hall1", rows=15, seats_in_row=20)
        sample_theatre_hall(name="Test hall2", rows=10, seats_in_row=15)

        response = self.client.get(THEATRE_HALL_URL)

        theatre_halls = TheatreHall.objects.all()
        serializer = TheatreHallSerializer(theatre_halls, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_theatre_hall_permitted(self):
        payload = {"name": "Test hall", "rows": 15, "seats_in_row": 20}
        response = self.client.post(THEATRE_HALL_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
