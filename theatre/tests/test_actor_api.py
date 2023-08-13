from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from theatre.models import Actor
from theatre.serializers import ActorSerializer


ACTOR_URL = reverse("theatre:actor-list")


def sample_actor(**params):
    defaults = {"first_name": "Test", "last_name": "Actor"}
    defaults.update(params)

    return Actor.objects.create(**defaults)


class UnauthenticatedActorApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(ACTOR_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedActorApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpassword",
        )
        self.client.force_authenticate(self.user)

    def test_actors_list_access(self):
        sample_actor(first_name="John1", last_name="Doe1")
        sample_actor(first_name="John2", last_name="Doe2")

        response = self.client.get(ACTOR_URL)

        actors = Actor.objects.all()
        serializer = ActorSerializer(actors, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_actor_forbidden(self):
        payload = {
            "first_name": "first",
            "last_name": "last"
        }
        response = self.client.post(ACTOR_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminActorApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            "admin@test.com",
            "testpassword",
        )
        self.client.force_authenticate(self.user)

    def test_actor_list_admin_access(self):
        sample_actor(first_name="John1", last_name="Doe1")
        sample_actor(first_name="John2", last_name="Doe2")

        response = self.client.get(ACTOR_URL)

        actors = Actor.objects.all()
        serializer = ActorSerializer(actors, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_actor_permitted(self):
        payload = {
            "first_name": "first",
            "last_name": "last"

        }
        response = self.client.post(ACTOR_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
