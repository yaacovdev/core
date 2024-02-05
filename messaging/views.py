from rest_framework import status
from rest_framework.generics import DestroyAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Message
from .serializers import MessageSerializer


class SendMessageView(APIView):
    """
    View for sending a message.

    Requires authentication.

    Methods:
    - post: Sends a message with the provided data.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(sender=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserMessagesListView(ListAPIView):
    """
    API view for retrieving messages for a specific user.
    Only authenticated users are allowed to access this view.
    """

    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        sent_messages = Message.objects.filter(sender=user)
        received_messages = Message.objects.filter(receiver=user)

        # Serialize the data
        sent_messages_serializer = self.get_serializer(sent_messages, many=True)
        received_messages_serializer = self.get_serializer(received_messages, many=True)

        return Response(
            {
                "sent_messages": sent_messages_serializer.data,
                "received_messages": received_messages_serializer.data,
            }
        )


class UnreadMessagesListView(ListAPIView):
    """
    API view to retrieve a list of unread messages for the authenticated user.
    """

    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        sent_messages = Message.objects.filter(sender=user, is_read=False)
        received_messages = Message.objects.filter(receiver=user, is_read=False)

        # Serialize the data
        sent_messages_serializer = self.get_serializer(sent_messages, many=True)
        received_messages_serializer = self.get_serializer(received_messages, many=True)

        return Response(
            {
                "sent_messages": sent_messages_serializer.data,
                "received_messages": received_messages_serializer.data,
            }
        )


class ReadMessageView(RetrieveAPIView):
    """
    View for reading a message.

    Retrieves a message object and updates its 'is_read' field to True if it is not already read.
    The receiver of the message can read and mark it as read. The sender can only mark it as read.
    Inherits from RetrieveAPIView class and uses MessageSerializer for serialization.
    Requires authentication for accessing the view.
    """

    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        message = self.get_object()

        if message.receiver != request.user and message.sender != request.user:
            return Response(
                {"message": "You can only read messages sent to or by you."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if message.receiver == request.user and not message.is_read:
            message.is_read = True
            message.save(update_fields=["is_read"])

        return self.retrieve(request, *args, **kwargs)


class DeleteMessageView(DestroyAPIView):
    """
    View for deleting a message.

    This view allows authenticated users to delete their own messages or messages they have sent.
    Only the receiver or sender of the message can delete it.

    Inherits from DestroyAPIView which provides the DELETE method implementation.

    Attributes:
        queryset (QuerySet): The queryset of all messages.
        serializer_class (Serializer): The serializer class for the message model.
        permission_classes (list): The list of permission classes for the view.

    Methods:
        delete: Deletes the message if the user is the receiver or sender.
    """

    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        message = self.get_object()
        if message.receiver == request.user or message.sender == request.user:
            return self.destroy(request, *args, **kwargs)
        else:
            return Response(
                {
                    "message": "You can only delete your own messages or messages you have sent."
                },
                status=status.HTTP_403_FORBIDDEN,
            )
