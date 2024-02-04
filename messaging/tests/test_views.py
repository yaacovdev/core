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
        # create a message for the user
        self.message = Message.objects.create(
            sender=self.user,
            receiver=self.user,
            subject="Test Subject",
            message="Test message content",
            is_read=False,
        )

    def test_get_user_messages_list_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Assuming 1 message for the user

    def test_get_user_messages_list_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UnreadMessagesListViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            "testuser", "testuser@example.com", "testpassword"
        )
        self.url = reverse("messaging:unread-messages-list")
        # Create a unred message for the user
        self.message = Message.objects.create(
            sender=self.user,
            receiver=self.user,
            subject="Test Subject",
            message="Test message content",
            is_read=False,
        )
        self.message.save()
        # Create a read message for the user
        self.read_message = Message.objects.create(
            sender=self.user,
            receiver=self.user,
            subject="Test Subject",
            message="Test message content",
            is_read=True,
        )
        self.read_message.save()

    def test_get_unread_messages_list_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_unread_messages_list_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_unread_messages_list_authenticated_with_unread_messages(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.message.id)
        self.assertEqual(response.data[0]["is_read"], False)


class ReadMessageViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            "testuser", "testuser@example.com", "testpassword"
        )
        self.message = Message.objects.create(
            sender=self.user,
            receiver=self.user,
            subject="Test Subject",
            message="Test message content",
            is_read=False,
        )
        self.url = reverse("messaging:read-message", kwargs={"pk": self.message.pk})

    def test_read_message_authenticated_receiver(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["is_read"], True)
        self.message.refresh_from_db()
        self.assertEqual(self.message.is_read, True)

    def test_read_message_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_read_message_authenticated_sender(self):
        sender = User.objects.create_user(
            "sender", "sender@example.com", "testpassword"
        )
        self.client.force_authenticate(user=sender)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.message.refresh_from_db()
        self.assertEqual(self.message.is_read, False)

    def test_read_message_authenticated_different_receiver(self):
        receiver = User.objects.create_user(
            "receiver", "receiver@example.com", "testpassword"
        )
        self.client.force_authenticate(user=receiver)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.message.refresh_from_db()
        self.assertEqual(self.message.is_read, False)

    def test_after_read_message_the_message_is_read(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.message.refresh_from_db()
        self.assertEqual(self.message.is_read, True)
