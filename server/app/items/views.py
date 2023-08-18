from django_filters import rest_framework as filters
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Item
from .serializers import ItemSerializer


class ItemListCreateView(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    filter_backends = [filters.DjangoFilterBackend]
    # TODO: フィルタのカスタム
    filterset_fields = "__all__"
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        images_data = self.request.data.get("image_set")
        serializer.save(images_data=images_data)


class ItemRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()

        if request.user == obj.seller or request.user.is_staff:
            return super().destroy(request, *args, **kwargs)

        return self.permission_denied(request)
