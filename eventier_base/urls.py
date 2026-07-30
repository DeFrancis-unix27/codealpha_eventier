from django.urls import path
from . import views
urlpatterns = [
    path("reg/",views.RegisterView.as_view()),
    path("log/",views.LoginView.as_view()),
    path("create_event/",views.EventCreateView.as_view()),
    path("list_event/",views.EventListView.as_view())
]
