# urls.py
from django.urls import path

from .views import (DeleteMessageView, ReadMessageView, SendMessageView,
                    UnreadMessagesListView, UserMessagesListView)

app_name = "messaging"
urlpatterns = [
    path("send/", SendMessageView.as_view(), name="send-message"),
    path("", UserMessagesListView.as_view(), name="user-messages-list"),
    path("unread/", UnreadMessagesListView.as_view(), name="unread-messages-list"),
    path("<int:pk>/", ReadMessageView.as_view(), name="read-message"),
    path("<int:pk>/delete/", DeleteMessageView.as_view(), name="delete-message"),
]
