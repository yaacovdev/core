from django.contrib.auth.models import User
from django.forms import ValidationError
from django.test import TestCase

from messaging.models import Message


class MessageModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create test users
        cls.sender = User.objects.create_user(username="sender", password="password")
        cls.receiver = User.objects.create_user(
            username="receiver", password="password"
        )

        # Create a test message
        cls.message = Message.objects.create(
            sender=cls.sender,
            receiver=cls.receiver,
            subject="Test Subject",
            message="Test Message",
            is_read=False,
        )

    def test_str_representation(self):
        expected_str = f"Message from {self.sender} to {self.receiver} - Test Subject"
        self.assertEqual(str(self.message), expected_str)

    def test_creation_date_auto_now_add(self):
        self.assertIsNotNone(self.message.creation_date)

    def test_is_read_default_value(self):
        message_without_is_read = Message.objects.create(
            sender=self.sender, receiver=self.receiver, subject="Test", message="Test"
        )
        self.assertFalse(message_without_is_read.is_read)

    def test_subject_cannot_be_blank(self):
        message_with_blank_subject = Message(
            sender=self.sender,
            receiver=self.receiver,
            subject="",
            message="Test Message",
            is_read=False,
        )

        with self.assertRaises(ValidationError):
            message_with_blank_subject.full_clean()

    def test_message_with_spaces_in_subject(self):
        message_with_spaces_subject = Message(
            sender=self.sender,
            receiver=self.receiver,
            subject="   ",
            message="Test Message",
            is_read=False,
        )

        with self.assertRaises(ValidationError):
            message_with_spaces_subject.full_clean()

    def test_message_cannot_be_blank(self):
        message_with_blank_message = Message(
            sender=self.sender,
            receiver=self.receiver,
            subject="Test Subject",
            message="",
            is_read=False,
        )

        with self.assertRaises(ValidationError):
            message_with_blank_message.full_clean()
