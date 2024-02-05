# urls.py
from django.urls import path

from . import views

app_name = "messaging"
urlpatterns = [
    path("send/", views.SendMessageView.as_view(), name="send-message"),
    path("", views.UserMessagesListView.as_view(), name="user-messages-list"),
    path(
        "unread/", views.UnreadMessagesListView.as_view(), name="unread-messages-list"
    ),
    path("<int:pk>/", views.ReadMessageView.as_view(), name="read-message"),
    path("<int:pk>/delete/", views.DeleteMessageView.as_view(), name="delete-message"),
]
