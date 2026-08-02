from rest_framework import serializers
from .models import CustomUser, Event, Chioce, CustomField, Attendee, CustomAnswer
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate
from django.utils import timezone

class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = (
            "id",
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

        validated_data.pop("confirm_password")
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
    organizer = serializers.CharField(source="event_orgs.username", read_only=True)

    class Meta:
        model = Event
        fields = "__all__"
        read_only_fields = ["event_orgs"]

    def validate(self, attrs):
        if attrs.get("start_date") < timezone.now():
            raise serializers.ValidationError(
                "sorry dear your event are in the past try bring it to the present of future"
                )
        if attrs.get("end_date") < attrs.get("start_date")
             raise ValueError("you can't end an event before it begins!")
        if attrs.get("end_date") < attrs.get("start_date"):
            raise serializers.ValidationError(
                "event can't end before start"
            ) 
        return attrs


class ChioceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chioce
        fields = "__all__"


class CustomFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomField
        fields = "__all__"


class AttendeeSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)
    event_id = serializers.PrimaryKeyRelatedField(
        queryset=Event.objects.all(), source="event", write_only=True
    )
    class Meta:
        model = Attendee
        fields = [
            "id",
            "event",
            "event_id",
            "firstname",
            "lastname",
            "email",
            "phone",
            "user",
            "is_guest",
            "date"
        ]

    def validate(self, attrs):
        user = attrs["user"]
        if not user:
            required = ["firstname", "lastname", "email"]
            for field in required:
                if not attrs.get(field):
                    raise serializers.ValidationError(
                        "{field} is required (if you have not registered yet )"
                    )
                user_email = attrs["email"] = user.user_email
                if self.email == user_email :
                    raise serializers.ValidationError(
                        "dear an account has uses this email"
                    )
        return attrs


class CustomAnswerSerializer(serializers.ModelSerializer):
    attendee = AttendeeSerializer(read_only=True)
    question = CustomFieldSerializer(read_only=True)

    attendee_id = serializers.PrimaryKeyRelatedField(
        queryset=Attendee.objects.all(),
        source="attendee",
        write_only=True,
    )
    question_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomField.objects.all(),
        source="question",
        write_only=True,
    )
    
    class Meta:
        model = CustomAnswer
        fields = [
            "id",
            "attendee",
            "question",
            "attendee_id",
            "question_id",
            "answer"
        ]

    def validate(self, attrs):
        if CustomAnswer.objects.filter(
            attendee=attrs["attendee"], question=attrs["question"]
        ).exists():
            raise ValueError(
                "sorry dear you can't answer one question two times thanks "
            )
        return attrs
