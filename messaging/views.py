from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
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

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(receiver=user)


class UnreadMessagesListView(ListAPIView):
    """
    API view to retrieve a list of unread messages for the authenticated user.
    """

    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(receiver=user, is_read=False)


class ReadMessageView(RetrieveAPIView):
    """
    View for reading a message.

    Retrieves a message object and updates its 'is_read' field to True if it is not already read.
    Only the receiver of the message can read it.

    Inherits from RetrieveAPIView class and uses MessageSerializer for serialization.
    Requires authentication for accessing the view.
    """

    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        message = self.get_object()
        if message.receiver != request.user:
            return Response(
                {"message": "We can only read your messages."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if not message.is_read:
            message.is_read = True
            message.save(update_fields=["is_read"])

        return self.retrieve(request, *args, **kwargs)
