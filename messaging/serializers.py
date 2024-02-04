from rest_framework import serializers

from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for the Message model.

    This serializer is used to convert Message objects into JSON representation and vice versa.
    It defines the fields that should be included in the serialized output and provides validation
    for the subject and message fields to ensure they are not empty or composed of only spaces.
    """

    class Meta:
        model = Message
        fields = [
            "id",
            "sender",
            "receiver",
            "subject",
            "message",
            "creation_date",
            "is_read",
        ]

    def validate_not_empty(self, value, field_name):
        """
        Validate that the field is not empty or composed of only spaces.
        """
        if value.isspace() or not value:
            raise serializers.ValidationError(
                f"The {field_name} cannot be empty or composed of only spaces."
            )
        return value

    def validate_subject(self, value):
        """
        Validate that the subject is not empty or composed of only spaces.
        """
        return self.validate_not_empty(value, "subject")

    def validate_message(self, value):
        """
        Validate that the message is not empty or composed of only spaces.
        """
        return self.validate_not_empty(value, "message")
