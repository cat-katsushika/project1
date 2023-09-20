from rest_framework import generics, permissions, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import Item, Like
from .serializers import ItemSerializer


class ItemListPagination(PageNumberPagination):
    page_size = 20
    max_page_size = 100


class ItemListCreateView(generics.ListCreateAPIView):
    queryset = Item.objects.all().order_by("-updated_at")
    serializer_class = ItemSerializer
    pagination_class = ItemListPagination

    # MEMO: コピペしただけなので、後で整理する
    def get_queryset(self):
        queryset = self.queryset
        name_query = self.request.query_params.get("name", None)
        if name_query:
            queryset = queryset.filter(name__icontains=name_query)
        return queryset


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


class ItemLikeToggleView(generics.UpdateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def partial_update(self, request, *args, **kwargs):
        item = self.get_object()
        user = request.user

        if user in item.liked_by.all():
            # instance.liked_by.remove(user)
            Like.objects.get(item=item, user=user).delete()
        else:
            # instance.liked_by.add(user)
            Like.objects.create(item=item, user=user)

        serializer = self.get_serializer(item)
        return Response(serializer.data)


class LikeItemListView(generics.ListAPIView):
    serializer_class = ItemSerializer

    def get_queryset(self):
        user = self.request.user
        liked_items = Item.objects.filter(liked_by__user=user)
        return liked_items
