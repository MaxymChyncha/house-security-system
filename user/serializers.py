from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=63, required=True)
    last_name = serializers.CharField(max_length=63, required=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "role"
        )
        extra_kwargs = {"write_only": True}

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        with transaction.atomic():
            role = validated_data.get("role").capitalize()
            user = User.objects.create_user(**validated_data)

            try:
                group = Group.objects.get(name=role)
                user.groups.add(group)
            except Group.DoesNotExist:
                raise serializers.ValidationError({"role": "Group does not exist."})

            return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user
