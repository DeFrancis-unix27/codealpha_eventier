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
from rest_framework import filters
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
from django.utils import timezone

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


class ListUsersView(generics.ListAPIView):
    serializer_class = RegisterSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]


class DeleteAccountView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

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



# get in to see event by id
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


# -----  end of event ------
class CreateChioce(CreateAPIView):
    queryset = Chioce.objects.all()
    serializer_class = ChioceSerializer
    permission_classes = [IsAuthenticated]


class ListChioce(generics.ListAPIView):
    queryset = Chioce.objects.all()
    serializer_class = ChioceSerializer
    permission_classes = [IsAuthenticated]


class RetriveChioce(generics.RetrieveAPIView):
    queryset = Chioce.objects.all()
    serializer_class = ChioceSerializer
    permission_classes = [IsAuthenticated]


class UpdateChioce(generics.UpdateAPIView):
    queryset = Chioce.objects.all()
    serializer_class = ChioceSerializer
    permission_classes = [IsAuthenticated]


class DeleteChioce(generics.DestroyAPIView):
    queryset = Chioce.objects.all()
    serializer_class = ChioceSerializer
    permission_classes = [IsAuthenticated]


# ------------------------------------ end Chioce -----------------------------------------------------------


class CreateCustomField(CreateAPIView):
    queryset = CustomField.objects.all()
    serializer_class = CustomFieldSerializer
    permission_classes = [IsAuthenticated]


class ListCustomField(generics.ListAPIView):
    queryset = CustomField.objects.all()
    serializer_class = CustomFieldSerializer
    permission_classes = [IsAuthenticated]


class RetriveCustomField(generics.RetrieveAPIView):
    queryset = CustomField.objects.all()
    serializer_class = CustomFieldSerializer
    permission_classes = [IsAuthenticated]


class UpdateCustomField(generics.UpdateAPIView):
    queryset = CustomField.objects.all()
    serializer_class = CustomFieldSerializer
    permission_classes = [IsAuthenticated]


class DeleteCustomField(generics.DestroyAPIView):
    queryset = CustomField.objects.all()
    serializer_class = CustomFieldSerializer
    permission_classes = [IsAuthenticated]


class CreateAttendee(CreateAPIView):
    queryset = Attendee.objects.all()
    serializer_class = AttendeeSerializer
    permission_classes = [AllowAny]


class ListAttendces(generics.ListAPIView):
    serializer_class = AttendeeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Attendee.objects.filter(event__event_orgs=self.request.user)


class RetriveAttendee(generics.RetrieveAPIView):
    serializer_class = AttendeeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Attendee.objects.filter(event__event_orgs=self.request.user)


class CreateCustomAnswer(CreateAPIView):
    serializer_class = CustomAnswerSerializer
    queryset = CustomAnswer.objects.all()
    permission_classes = [AllowAny]


class ListCustomAnswers(generics.ListAPIView):
    serializer_class = CustomAnswerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CustomAnswer.objects.filter(
            question__event__event_orgs=self.request.user
        )


class PublicView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = EventSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "start_date", "end_date"]

    def get_queryset(self):
        return Event.objects.filter(state="published")


class UserPalace(APIView):
    permission_classes: list = [IsAuthenticated]

    def get(self, request):
        user = request.user
        total_event = Event.objects.filter(event_orgs=user).count()
        published_event = Event.objects.filter(
            state="published", event_orgs=user
        ).count()
        draft_event = Event.objects.filter(state="draft", event_orgs=user).count()
        total_attendees = Attendee.objects.filter(event__event_orgs=user).count()
        upcoming_events = Event.objects.filter(state="published").order_by("start_date").first()
        recent_events = Event.objects.filter(event_orgs=user).order_by("start_date")[:7]
        recent_attendee = Attendee.objects.filter(event__event_orgs=user).order_by("date")
        return Response(
            {
                "total_event": total_event,
                "published_event": published_event,
                "draft_event": draft_event,
                "total_attendee": total_attendees,
                "upcoming_events": EventSerializer(upcoming_events).data if upcoming_events else None ,
                "recent_events": EventSerializer(recent_events,many=True).data,
                "recent_attendee": AttendeeSerializer(recent_attendee, many=True).data,
            }
        )
