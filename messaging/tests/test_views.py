from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import Message
from ..serializers import MessageSerializer


class SendMessageViewTestCase(APITestCase):
    def setUp(self):
        self.sender = User.objects.create_user(
            "sender", "sender@example.com", "testpassword"
        )
        self.receiver = User.objects.create_user(
            "receiver", "receiver@example.com", "testpassword"
        )
        self.url = reverse("messaging:send-message")
        self.valid_payload = {
            "sender": self.sender.id,
            "receiver": self.receiver.id,
            "subject": "Test Subject",
            "message": "Test message content",
            "creation_date": "2024-01-01T00:00:00Z",
            "is_read": False,
        }
        self.invalid_payload = {
            "sender": self.sender.id,
            "receiver": self.receiver.id,
            "subject": "",
            "message": "",
            "creation_date": "2024-01-01T00:00:00Z",
            "is_read": False,
        }

    def test_send_message_with_valid_payload(self):
        self.client.force_authenticate(user=self.sender)
        response = self.client.post(self.url, self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        message = Message.objects.get(subject=self.valid_payload["subject"])
        serializer = MessageSerializer(message)
        self.assertEqual(response.data, serializer.data)

    def test_send_message_with_invalid_payload(self):
        self.client.force_authenticate(user=self.sender)
        response = self.client.post(self.url, self.invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(set(response.data.keys()), set(["subject", "message"]))

    def test_send_message_without_authentication(self):
        response = self.client.post(self.url, self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UserMessagesListViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            "testuser", "testuser@example.com", "testpassword"
        )
        self.url = reverse("messaging:user-messages-list")

    def test_get_user_messages_list_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)  # Assuming no messages for the user

    def test_get_user_messages_list_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
