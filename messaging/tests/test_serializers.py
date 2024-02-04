from django.contrib.auth.models import User
from django.test import TestCase

from ..models import Message
from ..serializers import MessageSerializer


class MessageSerializerTestCase(TestCase):
    def setUp(self):
        # Créer des instances User pour sender et receiver
        self.sender = User.objects.create_user(
            "sender", "sender@example.com", "testpassword"
        )
        self.receiver = User.objects.create_user(
            "receiver", "receiver@example.com", "testpassword"
        )

        self.message_attributes = {
            "sender": self.sender,
            "receiver": self.receiver,
            "subject": "Test Subject",
            "message": "Test message content",
            "creation_date": "2023-01-01T00:00:00Z",
            "is_read": False,
        }

        self.serializer_data = {
            "sender": self.sender.id,
            "receiver": self.receiver.id,
            "subject": "Test Subject",
            "message": "Test message content",
            "creation_date": "2023-01-01T00:00:00Z",
            "is_read": False,
        }

        self.message = Message.objects.create(**self.message_attributes)
        self.serializer = MessageSerializer(instance=self.message)

    def test_contains_expected_fields(self):
        data = self.serializer.data

        self.assertEqual(
            set(data.keys()),
            set(
                [
                    "id",
                    "sender",
                    "receiver",
                    "subject",
                    "message",
                    "creation_date",
                    "is_read",
                ]
            ),
        )

    def test_subject_field_validation(self):
        self.serializer_data["subject"] = "   "
        serializer = MessageSerializer(data=self.serializer_data)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), set(["subject"]))

    def test_message_field_validation(self):
        self.serializer_data["message"] = ""
        serializer = MessageSerializer(data=self.serializer_data)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), set(["message"]))

    def test_valid_data_creates_message(self):
        serializer = MessageSerializer(data=self.serializer_data)

        self.assertTrue(serializer.is_valid())
        message = serializer.save()
        self.assertEqual(message.subject, self.serializer_data["subject"])
        self.assertEqual(message.message, self.serializer_data["message"])
