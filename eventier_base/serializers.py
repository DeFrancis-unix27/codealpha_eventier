from rest_framework import serializers
from .models import CustomUser, Event, Chioce, CustomField, Attendee, CustomAnswer
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate


class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = (
            "firstname",
            "lastname",
            "user_email",
            "username",
            "password",
            "confirm_password",
        )

        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"password": "are you sure? this passwords match"}
            )
        return attrs

    def create(self, validated_data):
    
        print(validated_data)
        validated_data.pop("confirm_password")

        print(validated_data)
        password = validated_data.pop("password")
        user = CustomUser.objects.create(**validated_data)

        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Invalid username or password")

        if not check_password(password, user.password):
            raise serializers.ValidationError("Invalid username and password")

        attrs["user"] = user
        return attrs


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"
        read_only_fields = ["event_orgs"]


class ChioceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chioce
        fields = "__all__"


class CustomFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomField
        fields = "__all__"


class AttendeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendee
        fields = "__all__"
        exclude = "date"
        extra_kwargs = {
            "firstname": {"required": True},
            "lastname": {"required": True},
            "email": {"required": True},
            "phone": {"required": True},
        }


class CustomAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomAnswer
        fields = "__all__"
