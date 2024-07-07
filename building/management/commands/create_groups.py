from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from building.models import Building, Entrance, Apartment


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.admin_group, _ = Group.objects.get_or_create(name="Admin")
        self.manager_group, _ = Group.objects.get_or_create(name="Manager")
        self.guard_group, _ = Group.objects.get_or_create(name="Guard")

        self._add_building_permissions()
        self._add_entrance_permissions()
        self._add_apartment_permissions()

        self.stdout.write(self.style.SUCCESS("Groups and permissions have been set up."))

    def _add_building_permissions(self):
        building_permissions = self._get_building_permissions()

        for permission in building_permissions:
            if permission.codename == "view_building":
                self.admin_group.permissions.add(permission)
                self.manager_group.permissions.add(permission)

            else:
                self.admin_group.permissions.add(permission)

    def _add_entrance_permissions(self):
        entrance_permissions = self._get_entrance_permissions()

        for permission in entrance_permissions:
            if permission.codename == "view_entrance":
                self.admin_group.permissions.add(permission)
                self.manager_group.permissions.add(permission)
                self.guard_group.permissions.add(permission)

            elif permission.codename == "assign_guard":
                self.admin_group.permissions.add(permission)
                self.manager_group.permissions.add(permission)

            else:
                self.admin_group.permissions.add(permission)

    def _add_apartment_permissions(self):
        apartment_permissions = self._get_apartment_permissions()

        for permission in apartment_permissions:
            if permission.codename == "view_apartment":
                self.admin_group.permissions.add(permission)
                self.manager_group.permissions.add(permission)
                self.guard_group.permissions.add(permission)

            else:
                self.admin_group.permissions.add(permission)

    @staticmethod
    def _get_building_permissions():
        content_type = ContentType.objects.get_for_model(Building)
        building_permissions = Permission.objects.filter(content_type=content_type)

        return building_permissions

    @staticmethod
    def _get_entrance_permissions():
        content_type = ContentType.objects.get_for_model(Entrance)
        entrance_permissions = Permission.objects.filter(content_type=content_type)

        return entrance_permissions

    @staticmethod
    def _get_apartment_permissions():
        content_type = ContentType.objects.get_for_model(Apartment)
        apartment_permissions = Permission.objects.filter(content_type=content_type)

        return apartment_permissions
