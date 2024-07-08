from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from building.models import Building, Entrance, Apartment

User = get_user_model()
ENTRANCE_API_URL = reverse("building:entrance-list")


def detail_url(entrance_id):
    return reverse("building:entrance-detail", args=[entrance_id])


class EntranceViewSetTests(APITestCase):

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
            number=102
        )
        self.client = APIClient()

    def test_list_entrances_as_admin(self):
        self.client.force_authenticate(self.admin)
        res = self.client.get(ENTRANCE_API_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)

    def test_list_entrances_as_manager(self):
        # Manager's entrance
        self.client.force_authenticate(self.manager)
        res = self.client.get(ENTRANCE_API_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["building"], self.building.address)

        # No Manager's entrance
        new_building = Building.objects.create(address="New Address")
        Entrance.objects.create(number=102, building=new_building)

        res = self.client.get(ENTRANCE_API_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)

    def test_list_entrances_as_guard(self):
        # Guard's entrance
        self.client.force_authenticate(self.guard)
        res = self.client.get(ENTRANCE_API_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["guard"], self.guard.full_name)

        # No Guard's Entrance
        Entrance.objects.create(number=103, building=self.building)

        res = self.client.get(ENTRANCE_API_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(res.data), 1)

    def test_retrieve_entrance_as_admin(self):
        self.client.force_authenticate(self.admin)
        url = detail_url(self.entrance.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["id"], self.entrance.id)

    def test_retrieve_entrance_as_manager(self):
        self.client.force_authenticate(self.manager)
        url = detail_url(self.entrance.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["id"], self.entrance.id)
        self.assertEqual(res.data["building"], self.building.address)

    def test_retrieve_entrance_as_guard(self):
        self.client.force_authenticate(self.guard)
        url = detail_url(self.entrance.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["id"], self.entrance.id)
        self.assertEqual(res.data["guard"], self.guard.full_name)

    def test_create_entrance_as_admin(self):
        self.client.force_authenticate(self.admin)
        data = {
            "number": 2,
            "building": self.building.id,
            "guard": self.guard.id
        }
        res = self.client.post(ENTRANCE_API_URL, data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Entrance.objects.filter(number=2).exists())

    def test_create_entrance_as_non_admin(self):
        self.client.force_authenticate(self.manager)
        data = {
            "number": 2,
            "building": self.building.id,
            "guard": self.guard.id
        }
        res = self.client.post(ENTRANCE_API_URL, data)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_entrance_as_admin(self):
        self.client.force_authenticate(self.admin)
        url = detail_url(self.entrance.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Entrance.objects.filter(id=self.entrance.id).exists())

    def test_delete_entrance_as_non_admin(self):
        self.client.force_authenticate(self.manager)
        url = detail_url(self.entrance.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Entrance.objects.filter(id=self.entrance.id).exists())

    def test_update_entrance_as_admin(self):
        self.client.force_authenticate(self.admin)
        url = detail_url(self.entrance.id)
        data = {"number": 10}

        res = self.client.patch(url, data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.entrance.refresh_from_db()
        self.assertEqual(self.entrance.number, 10)

    def test_update_entrance_as_manager(self):
        self.client.force_authenticate(self.manager)
        url = detail_url(self.entrance.id)
        data = {"number": 10}

        res = self.client.patch(url, data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.entrance.refresh_from_db()
        self.assertEqual(self.entrance.number, 10)
        self.assertEqual(self.entrance.building, self.building)
