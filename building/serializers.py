from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from building.models import Building, Entrance, Apartment


class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = ("id", "address", "manager",)

    def validate(self, data):
        manager = data.get("manager")
        if manager and manager.role != "manager":
            raise ValidationError(
                {"manager": "The assigned user must have the role of 'manager'."}
            )

        return data


class EntranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entrance
        fields = ("id", "building", "number", "guard",)

    def validate(self, data):
        guard = data.get("guard")
        if guard and guard.role != "guard":
            raise ValidationError(
                {"guard": "The assigned user must have the role of 'guard'."}
            )

        return data


class ApartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apartment
        fields = ("id", "entrance", "number",)


class EntranceListSerializer(EntranceSerializer):
    building = serializers.SlugRelatedField(read_only=True, slug_field="address")
    guard = serializers.SlugRelatedField(read_only=True, slug_field="full_name")
    apartments = ApartmentSerializer(many=True, read_only=True)

    class Meta(EntranceSerializer.Meta):
        fields = EntranceSerializer.Meta.fields + ("apartments",)


class BuildingListSerializer(BuildingSerializer):
    manager = serializers.SlugRelatedField(read_only=True, slug_field="full_name")
    entrances = EntranceListSerializer(many=True, read_only=True)

    class Meta(BuildingSerializer.Meta):
        fields = BuildingSerializer.Meta.fields + ("entrances",)
