from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import MessageSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView
from .models import Message


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
