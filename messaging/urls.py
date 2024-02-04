# urls.py
from django.urls import path
from .views import SendMessageView


app_name = "messaging"
urlpatterns = [
    path("send/", SendMessageView.as_view(), name="send-message"),
]
