# urls.py
from django.urls import path

from .views import (ReadMessageView, SendMessageView, UnreadMessagesListView,
                    UserMessagesListView)

app_name = "messaging"
urlpatterns = [
    path("send/", SendMessageView.as_view(), name="send-message"),
    path("inbox/", UserMessagesListView.as_view(), name="user-messages-list"),
    path(
        "inbox/unread/", UnreadMessagesListView.as_view(), name="unread-messages-list"
    ),
    path("inbox/<int:pk>/", ReadMessageView.as_view(), name="read-message"),
]
