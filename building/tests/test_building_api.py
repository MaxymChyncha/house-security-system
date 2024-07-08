from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from building.models import Building, Entrance, Apartment

User = get_user_model()
BUILDING_API_URL = reverse("building:building-list")


def detail_url(building_id):
    return reverse("building:building-detail", args=[building_id])


class BuildingViewSetTests(APITestCase):

    def setUp(self):
        self.admin = User.objects.create_user(
            username="admin",
            first_name="admin",
            last_name="test",
            password="test1234",
            role="admin"
        )
        self.manager = User.objects.create_user(
            username="manager",
            first_name="manager",
            last_name="test",
            password="test1234",
            role="manager"
        )
        self.guard = User.objects.create_user(
            username="guard",
            first_name="guard",
            last_name="test",
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

    def test_list_buildings_as_admin(self):
        self.client.force_authenticate(self.admin)
        res = self.client.get(BUILDING_API_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)

    def test_list_buildings_as_manager(self):
        # Manager's buildings
        self.client.force_authenticate(self.manager)
        res = self.client.get(BUILDING_API_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["manager"], self.manager.full_name)

        # No Manager's buildings
        Building.objects.create(address="123 Test St")
        res = self.client.get(BUILDING_API_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)

    def test_list_buildings_as_guard(self):
        self.client.force_authenticate(self.guard)
        res = self.client.get(BUILDING_API_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_building_as_admin(self):
        self.client.force_authenticate(self.admin)
        url = detail_url(self.building.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["id"], self.building.id)

    def test_retrieve_building_as_manager(self):
        # Manager's building
        self.client.force_authenticate(self.manager)
        url = detail_url(self.building.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["id"], self.building.id)

        # No Manager's building
        another_building = Building.objects.create(address="123 Test St")
        url = detail_url(another_building.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_building_as_admin(self):
        self.client.force_authenticate(self.admin)
        data = {
            "address": "456 New St",
            "manager": self.manager.id
        }
        res = self.client.post(BUILDING_API_URL, data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Building.objects.filter(address="456 New St").exists())

    def test_create_building_as_non_admin(self):
        self.client.force_authenticate(self.manager)
        data = {
            "address": "456 New St",
            "manager": self.manager.id
        }
        res = self.client.post(BUILDING_API_URL, data)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_building_as_admin(self):
        self.client.force_authenticate(self.admin)
        url = detail_url(self.building.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Building.objects.filter(id=self.building.id).exists())

    def test_delete_building_as_non_admin(self):
        self.client.force_authenticate(self.manager)
        url = detail_url(self.building.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Building.objects.filter(id=self.building.id).exists())

    def test_update_building_as_admin(self):
        self.client.force_authenticate(self.admin)
        url = detail_url(self.building.id)
        data = {"address": "new_address"}

        res = self.client.patch(url, data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.building.refresh_from_db()
        self.assertEqual(self.building.address, "new_address")

    def test_update_building_as_manager(self):
        self.client.force_authenticate(self.manager)
        url = detail_url(self.building.id)
        data = {"address": "new_address"}

        res = self.client.patch(url, data)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.building.refresh_from_db()
        self.assertEqual(self.building.address, "123 Test St")
        self.assertEqual(self.building.manager, self.manager)
