from django_filters import rest_framework as filters
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .models import Item
from .serializers import ItemSerializer


class ItemListCreateView(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    filter_backends = [filters.DjangoFilterBackend]
    # TODO: フィルタのカスタム
    filterset_fields = "__all__"


class IsOwnerOrAdminOrReadOnly(permissions.BasePermission):
    message = "出品者しか編集できません。"

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.seller or request.user.is_staff


class ItemRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsOwnerOrAdminOrReadOnly]


class ItemPurchaseView(generics.UpdateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def update(self, request, *args, **kwargs):
        item = self.get_object()

        if item.seller == request.user:
            return Response({"error": "自分自身の商品を購入することはできません。"}, status=status.HTTP_400_BAD_REQUEST)

        item.buyer = request.user
        item.listing_status = Item.ListingStatus.PURCHASED
        item.save()

        serializer = self.get_serializer(item)
        return Response(serializer.data)
    

class ItemCancelView(generics.UpdateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def update(self, request, *args, **kwargs):
        item = self.get_object()

        if item.seller != request.user:
            return Response({"error": "自分の商品以外はキャンセルできません。"}, status=status.HTTP_400_BAD_REQUEST)

        item.buyer = None
        item.listing_status = Item.ListingStatus.UNPURCHASED
        item.save()

        serializer = self.get_serializer(item)
        return Response(serializer.data)
    

class ItemCompleteView(generics.UpdateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def update(self, request, *args, **kwargs):
        item = self.get_object()

        if item.buyer != request.user:
            # TODO: エラーメッセージを追加する
            return Response({"error": ""}, status=status.HTTP_400_BAD_REQUEST)

        item.listing_status = Item.ListingStatus.COMPLETED
        item.save()

        serializer = self.get_serializer(item)
        return Response(serializer.data)
