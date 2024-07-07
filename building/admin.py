from django.contrib import admin
from building.models import Building, Entrance, Apartment


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ("address", "manager",)
    list_filter = ("manager",)


@admin.register(Entrance)
class EntranceAdmin(admin.ModelAdmin):
    list_display = ("number", "building", "guard",)
    list_filter = ("building", "guard",)


@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    list_display = ("number", "entrance",)
    list_filter = ("entrance",)
