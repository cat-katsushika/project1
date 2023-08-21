from django_filters import rest_framework as filters
from rest_framework import generics

from .models import Item
from .serializers import ItemSerializer


class ItemListCreateView(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    filter_backends = [filters.DjangoFilterBackend]
    # TODO: フィルタのカスタム
    filterset_fields = "__all__"


class ItemRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    """
    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()

        if request.user == obj.seller or request.user.is_staff:
            return super().destroy(request, *args, **kwargs)

        return self.permission_denied(request)
    """
