# class Performance(models.Model):
#     play = models.ForeignKey(Play, on_delete=models.CASCADE)
#     theatre_hall = models.ForeignKey(TheatreHall, on_delete=models.CASCADE)
#     show_time = models.DateTimeField()
#



from django.contrib.auth import get_user_model
from django.db.models import F, Count
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from theatre.models import Play, Genre, Actor, TheatreHall, Performance
from theatre.serializers import PerformanceSerializer, PerformanceListSerializer, PerformanceDetailSerializer

PERFORMANCE_URL = reverse("theatre:performance-list")


def sample_play(**params):
    defaults = {
        "title": "Sample play",
        "description": "Sample description",
    }
    defaults.update(params)

    return Play.objects.create(**defaults)


def sample_performance(**params):
    play = sample_play()
    theatre_hall = TheatreHall.objects.create(
        name="Test theatre", rows=20, seats_in_row=20
    )

    defaults = {
        "play": play,
        "theatre_hall": theatre_hall,
        "show_time": "2022-06-02",
    }
    defaults.update(params)

    return Performance.objects.create(**defaults)

def get_performances():
    return Performance.objects.all().annotate(
        tickets_available=(
            F("theatre_hall__rows")
            * F("theatre_hall__seats_in_row")
            - Count("tickets")
        )
    )

def detail_url(performance_id):
    return reverse("theatre:performance-detail", args=[performance_id])


class UnauthenticatedPlayApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(PERFORMANCE_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedPlayApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpassword",
        )
        self.client.force_authenticate(self.user)

    def test_performances_list_access(self):

        sample_performance()
        sample_performance()

        response = self.client.get(PERFORMANCE_URL)

        performances = get_performances()
        serializer = PerformanceListSerializer(performances, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_filter_performances_by_play(self):
        play1 = sample_play(title="Play1")
        play2 = sample_play(title="Play2")
        play3 = sample_play(title="Test title")

        sample_performance(play=play1)
        sample_performance(play=play2)
        sample_performance(play=play3)

        response = self.client.get(PERFORMANCE_URL, {"play": "pl"})
        performances = get_performances()
        serializer = PerformanceListSerializer(performances, many=True)

        serializer1 = serializer.data[0]
        serializer2 = serializer.data[1]
        serializer3 = serializer.data[2]

        self.assertIn(serializer1, response.data)
        self.assertIn(serializer2, response.data)
        self.assertNotIn(serializer3, response.data)

    def test_filter_plays_by_date(self):
        sample_performance()
        sample_performance()
        sample_performance(show_time="2023-07-08", )

        response = self.client.get(PERFORMANCE_URL, {"date": "2022-06-02"})
        performances = get_performances()
        serializer = PerformanceListSerializer(performances, many=True)

        serializer1 = serializer.data[0]
        serializer2 = serializer.data[1]
        serializer3 = serializer.data[2]

        self.assertIn(serializer1, response.data)
        self.assertIn(serializer2, response.data)
        self.assertNotIn(serializer3, response.data)

    def test_create_play_forbidden(self):
        payload = {
            "play": "",
            "theatre_hall": "",
            "show_time": "2022-06-02",
        }
        response = self.client.post(PERFORMANCE_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminPerformanceApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            "admin@test.com",
            "testpassword",
        )
        self.client.force_authenticate(self.user)

    def test_performance_list_admin_access(self):
        sample_performance()
        sample_performance()

        response = self.client.get(PERFORMANCE_URL)

        performances = get_performances()
        serializer = PerformanceListSerializer(performances, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_performance_permitted(self):
        play = sample_play()
        theatre_hall = TheatreHall.objects.create(
            name="Test theatre", rows=20, seats_in_row=20
        )
        payload = {
            "play": play.id,
            "theatre_hall": theatre_hall.id,
            "show_time": "2022-06-02",
        }
        response = self.client.post(PERFORMANCE_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
