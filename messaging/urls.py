# urls.py
from django.urls import path

from .views import SendMessageView, UserMessagesListView

app_name = "messaging"
urlpatterns = [
    path("send/", SendMessageView.as_view(), name="send-message"),
    path("inbox/", UserMessagesListView.as_view(), name="user-messages-list"),
]
