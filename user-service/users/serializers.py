from rest_framework import serializers
from .models import User


class RegisterationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["id", "email", "password", "username", "phone_number"]

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "phone_number",
            "address",
            "loyalty_points",
        ]
        read_only_fields = ["id", "email", "loyalty_points"]
