from django.shortcuts import render
from .models import CustomUser, Attendee, CustomField, CustomAnswer, Chioce, Event
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    EventSerializer,
    AttendeeSerializer,
    CustomFieldSerializer,
    CustomAnswerSerializer,
    ChioceSerializer,
)
from rest_framework import generics
from rest_framework.generics import CreateAPIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import BasePermission
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth import logout
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.


# ============================== utlity
class Owned(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.event_orgs == request.user


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "message": "Login successfull",
                "user": {
                    "username": user.username,
                    "email": user.user_email,
                },
                "refresh_token": str(refresh),
                "refresh_access_token": str(refresh.access_token),
            },
            status=status.HTTP_200_OK,
        )


class DeleteAccountView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response(
            {"message": f"you have been logged out {self.request.user}"},
            status=status.HTTP_200_OK,
        )


# create event
class EventCreateView(CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        serializer.save(event_orgs=self.request.user)


# listing of event = {
# lis all events
class EventListView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [AllowAny]


# list all published events only
class PublishedEventListView(generics.ListAPIView):
    queryset = Event.objects.filter(published=True)
    serializer_class = EventSerializer
    permission_classes = [AllowAny]


# list all completed events only
class CompletedEventListView(generics.ListAPIView):
    queryset = Event.objects.filter(completed=True)
    serializer_class = EventSerializer
    permission_classes = [AllowAny]


# list all cancelled events only
class CancelledEventListView(generics.ListAPIView):
    queryset = Event.objects.filter(cancelled=True)
    serializer_class = EventSerializer
    permission_classes = [AllowAny]


# }


# get in to see event by pk
class RetriveEventView(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [AllowAny]


# updating event


class UpdateEventView(generics.UpdateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, Owned]


class DeleteEventView(generics.DestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, Owned]


class CreateChioce(CreateAPIView):
    queryset = Chioce
    serializer_class = ChioceSerializer
    permission_classes = [IsAuthenticated]


class RetriveChioce(generics.RetrieveAPIView):
    queryset = Chioce
    serializer_class = ChioceSerializer
    permission_classes = [IsAuthenticated]


class UpdateChioce(generics.UpdateAPIView):
    queryset = Chioce
    serializer_class = ChioceSerializer
    permission_classes = [IsAuthenticated]


class DeleteChioce(generics.DestroyAPIView):
    queryset = Chioce
    serializer_class = ChioceSerializer
    permission_classes = [IsAuthenticated]


# ------------------------------------Chioce -----------------------------------------------------------


class CreateCustomField(CreateAPIView):
    queryset = CustomField
    serializer_class = CustomFieldSerializer
    permission_classes = [IsAuthenticated]


class RetriveCustomField(generics.RetrieveAPIView):
    queryset = CustomField
    serializer_class = CustomFieldSerializer
    permission_classes = [IsAuthenticated]


class UpdateCustomField(generics.UpdateAPIView):
    queryset = CustomField
    serializer_class = CustomFieldSerializer
    permission_classes = [IsAuthenticated]


class DeleteCustomField(generics.DestroyAPIView):
    queryset = CustomField
    serializer_class = CustomFieldSerializer
    permission_classes = [IsAuthenticated]
