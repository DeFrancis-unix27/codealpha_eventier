from django.urls import path
from . import views

urlpatterns = [
    path("reg/", views.RegisterView.as_view()),
    path("log/", views.LoginView.as_view()),
    path("create_event/", views.EventCreateView.as_view()),
    path("event/<uuid:pk>/", views.RetriveEventView.as_view()),
    path("update_event/<uuid:pk>/", views.UpdateEventView.as_view()),
    path("delete_event/<uuid:pk>/", views.DeleteEventView.as_view()),
    path("create_chioce/", views.CreateChioce.as_view()),
    path("list_chioce/", views.ListChioce.as_view()),
    path("retrive_chioce/<int:pk>/", views.RetriveChioce.as_view()),
    path("update_chioce/<int:pk>/", views.UpdateChioce.as_view()),
    path("delete_chioce/<int:pk>/", views.DeleteChioce.as_view()),
    path("create_customfield/", views.CreateCustomField.as_view()),
    path("list_customfield/", views.ListCustomField.as_view()),
    path("retrive_customfield/<uuid:pk>/", views.RetriveCustomField.as_view()),
    path("update_customfield/<uuid:pk>/", views.UpdateCustomField.as_view()),
    path("delete_customfield/<uuid:pk>/", views.DeleteCustomField.as_view()),
    path("create_attendee/", views.CreateAttendee.as_view()),
    path("list_attendees/", views.ListAttendces.as_view()),
    path("retrive_attendee/<uuid:pk>/", views.RetriveAttendee.as_view()),
    path("create_customanswer/", views.CreateCustomAnswer.as_view()),
    path("list_customanswers/", views.ListCustomAnswers.as_view()),
    path("", views.PublicView.as_view()),
    path("my/",views.UserPalace.as_view()),

    # debug pupose only
    path("list_users/",views.ListUsersView.as_view())
]
