from rest_framework import generics, permissions, status, views
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

    def get_queryset(self):
        queryset = self.queryset
        name_query = self.request.query_params.get("name", None)
        listing_status_query = self.request.query_params.get("listing_status", None)
        if name_query:
            queryset = queryset.filter(name__icontains=name_query)
        if listing_status_query:
            queryset = queryset.filter(listing_status=listing_status_query)
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
    permission_classes = [IsOwnerOrAdminOrReadOnly]

    def update(self, request, *args, **kwargs):
        item = self.get_object()

        item.buyer = None
        item.listing_status = Item.ListingStatus.CANCELED
        item.save()

        serializer = self.get_serializer(item)
        return Response(serializer.data)


class ItemCompleteView(generics.UpdateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def update(self, request, *args, **kwargs):
        item = self.get_object()

        if item.buyer != request.user:
            return Response({"error": "購入者以外は購入完了できません。"}, status=status.HTTP_400_BAD_REQUEST)

        item.listing_status = Item.ListingStatus.COMPLETED
        item.save()

        serializer = self.get_serializer(item)
        return Response(serializer.data)


class ItemLikeToggleView(views.APIView):
    def post(self, request, *args, **kwargs):
        item_id = kwargs["pk"]
        user_id = request.user.id

        if not Item.objects.filter(id=item_id).exists():
            return Response({"error": "商品が存在しません。"}, status=status.HTTP_400_BAD_REQUEST)

        if Like.objects.filter(item_id=item_id, user_id=user_id).exists():
            Like.objects.filter(item_id=item_id, user_id=user_id).delete()
            return Response({"message": "いいねを取り消しました。"})
        else:
            Like.objects.create(item_id=item_id, user_id=user_id)
            return Response({"message": "いいねしました。"})


class UserLikeItemListView(generics.ListAPIView):
    serializer_class = ItemSerializer
    pagination_class = ItemListPagination
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        like_items = Item.objects.filter(liked_by__user=user).prefetch_related("liked_by")
        return like_items


class UserSellItemListView(generics.ListAPIView):
    serializer_class = ItemSerializer
    pagination_class = ItemListPagination
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        sell_items = Item.objects.filter(seller=user).select_related("seller")
        return sell_items


class UserBuyItemListView(generics.ListAPIView):
    serializer_class = ItemSerializer
    pagination_class = ItemListPagination
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        buy_items = Item.objects.filter(buyer=user).select_related("buyer")
        return buy_items
