from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Comment
from .serializers import CommentSerializer


class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class CommentListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        comments = Comment.objects.all()

        # item_idクエリパラメータが存在すればフィルタリング
        item_id = request.query_params.get("item_id", None)
        if item_id:
            comments = comments.filter(item_id=item_id)

        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
