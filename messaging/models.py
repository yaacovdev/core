from django.conf import settings
from django.db import models
from django.forms import ValidationError


class Message(models.Model):
    """
    Represents a message sent between users.

    Attributes:
        sender (User): The user who sent the message.
        receiver (User): The user who received the message.
        subject (str): The subject of the message.
        message (str): The content of the message.
        creation_date (datetime): The date and time when the message was created.
        is_read (bool): Indicates whether the message has been read or not.
    """

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="sent_messages", on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="received_messages",
        on_delete=models.CASCADE,
    )
    subject = models.CharField(max_length=255, blank=False)
    message = models.TextField(blank=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver} - {self.subject}"

    class Meta:
        ordering = ["-creation_date"]

    def clean(self):
        self.subject = self.subject.strip()

        if not self.subject:
            raise ValidationError(
                {"subject": "The subject cannot be empty or composed of only spaces."}
            )
        self.message = self.message.strip()
        if not self.message:
            raise ValidationError(
                {"message": "The message cannot be empty or composed of only spaces."}
            )

        super().clean()
