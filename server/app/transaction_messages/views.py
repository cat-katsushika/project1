from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Message
from .serializers import MessageSerializer


class MessageCreateView(generics.CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class MessageListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        messages = Message.objects.all()

        # item_idクエリパラメータが存在すればフィルタリング
        item_id = request.query_params.get("item_id", None)
        if item_id:
            messages = messages.filter(item_id=item_id)

        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
