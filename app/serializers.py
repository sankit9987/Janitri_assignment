from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Patient, HeartRate


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8,
    )

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "password",
        )

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
        )
        return user


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = (
            "id",
            "first_name",
            "last_name",
            "date_of_birth",
            "created_by",
            "created_at",
        )
        read_only_fields = (
            "id",
            "created_by",
            "created_at",
        )

    def create(self, validated_data):
        request = self.context.get("request")
        if request and hasattr(request, "user") and request.user.is_authenticated:
            validated_data["created_by"] = request.user
        return super().create(validated_data)


class HeartRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeartRate
        fields = (
            "id",
            "patient",
            "bpm",
            "recorded_at",
            "note",
            "created_at",
        )
        read_only_fields = ("id", "created_at")

    def validate_bpm(self, value):
        if not (20 <= value <= 250):
            raise serializers.ValidationError(
                "bpm must be between 20 and 250",
            )
        return value
