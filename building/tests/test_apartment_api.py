from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from building.models import Building, Entrance, Apartment


User = get_user_model()
APARTMENT_API_URL = reverse("building:apartment-list")


def detail_url(apartment_id):
    return reverse("building:apartment-detail", args=[apartment_id])


class ApartmentViewSetTests(APITestCase):

    def setUp(self):
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
        self.building = Building.objects.create(
            address="123 Test St",
            manager=self.manager
        )
        self.entrance = Entrance.objects.create(
            number=1,
            building=self.building,
            guard=self.guard
        )
        self.apartment = Apartment.objects.create(
            entrance=self.entrance,
            number=101
        )
        self.client = APIClient()

    def test_list_apartments_as_admin(self):
        self.client.force_authenticate(self.admin)
        res = self.client.get(APARTMENT_API_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)

    def test_list_apartments_as_manager(self):
        self.client.force_authenticate(self.manager)
        res = self.client.get(APARTMENT_API_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["entrance"], self.entrance.id)

    def test_list_apartments_as_guard(self):
        self.client.force_authenticate(self.guard)
        res = self.client.get(APARTMENT_API_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["entrance"], self.entrance.number)

    def test_retrieve_apartment_as_admin(self):
        self.client.force_authenticate(self.admin)
        url = detail_url(self.apartment.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["id"], self.apartment.id)

    def test_retrieve_apartment_as_manager(self):
        self.client.force_authenticate(self.manager)
        url = detail_url(self.apartment.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["id"], self.apartment.id)
        self.assertEqual(res.data["entrance"], self.entrance.number)

    def test_retrieve_apartment_as_guard(self):
        self.client.force_authenticate(self.guard)
        url = detail_url(self.apartment.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["id"], self.apartment.id)
        self.assertEqual(res.data["entrance"], self.entrance.number)

    def test_create_apartment_as_admin(self):
        self.client.force_authenticate(self.admin)
        data = {
            "number": 102,
            "entrance": self.entrance.id
        }
        res = self.client.post(APARTMENT_API_URL, data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Apartment.objects.filter(number=102).exists())

    def test_create_apartment_as_non_admin(self):
        self.client.force_authenticate(self.manager)
        data = {
            "number": 102,
            "entrance": self.entrance.id
        }
        res = self.client.post(APARTMENT_API_URL, data)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_apartment_as_admin(self):
        self.client.force_authenticate(self.admin)
        url = detail_url(self.apartment.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Apartment.objects.filter(id=self.apartment.id).exists())

    def test_delete_apartment_as_non_admin(self):
        self.client.force_authenticate(self.manager)
        url = detail_url(self.apartment.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Apartment.objects.filter(id=self.apartment.id).exists())

    def test_update_apartment_as_admin(self):
        self.client.force_authenticate(self.admin)
        url = detail_url(self.apartment.id)
        data = {"number": 202}

        res = self.client.patch(url, data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.apartment.refresh_from_db()
        self.assertEqual(self.apartment.number, 202)

    def test_update_apartment_as_manager(self):
        self.client.force_authenticate(self.manager)
        url = detail_url(self.apartment.id)
        data = {"number": 202}

        res = self.client.patch(url, data)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
