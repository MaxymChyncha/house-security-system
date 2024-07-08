from django.test import TestCase

from building.models import Entrance, Apartment, Building


class BuildingModelTests(TestCase):

    def setUp(self):
        self.building = Building.objects.create(address="123 Main St")

    def test_building_str(self):
        self.assertEqual(
            str(self.building),
            self.building.address
        )


class EntranceModelTests(TestCase):

    def setUp(self):
        self.building = Building.objects.create(address="123 Main St")
        self.entrance = Entrance.objects.create(number=1, building=self.building)

    def test_entrance_str(self):
        self.assertEqual(
            str(self.entrance),
            f"Building: {self.entrance.building.address}, Number: {self.entrance.number}"
        )


class ApartmentModelTests(TestCase):

    def setUp(self):
        self.building = Building.objects.create(address="123 Main St")
        self.entrance = Entrance.objects.create(number=1, building=self.building)
        self.apartment = Apartment.objects.create(entrance=self.entrance, number=1)

    def test_apartment_str(self):
        self.assertEqual(
            str(self.apartment),
            f"Entrance: {self.apartment.entrance.number}, "
            f"Number: {self.apartment.number}"
        )
