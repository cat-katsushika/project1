from rest_framework import generics, permissions, status, views
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Item, Like
from .serializers import ItemCreateSerializer, ItemSerializer


class ItemListPagination(PageNumberPagination):
    page_size = 20
    max_page_size = 100


class ItemListView(generics.ListAPIView):
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


class ItemCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # request.dataを変更可能な辞書にコピー
        data = dict(request.data.lists())
        # Itemの作成に必要なキー
        keys_to_check = [
            "price",
            "name",
            "description",
            "condition",
            "writing_state",
            "receivable_campus",
        ]
        # キーが辞書に存在しないときエラーを返す
        for key in keys_to_check:
            if key not in data:
                return Response({"error": f"{key} が必要です"}, status=status.HTTP_400_BAD_REQUEST)

        data["seller"] = request.user.id
        data["listing_status"] = Item.ListingStatus.UNPURCHASED
        data["price"] = data["price"][0]
        data["name"] = data["name"][0]
        data["description"] = data["description"][0]
        data["condition"] = data["condition"][0]
        data["writing_state"] = data["writing_state"][0]
        data["receivable_campus"] = data["receivable_campus"][0]

        if "image_1" not in data:
            return Response({"error": "写真が必須です。"}, status=status.HTTP_400_BAD_REQUEST)
        data["images"] = []
        data["images"].append({"photo_path": data.pop("image_1")[0], "order": 1})
        # 10枚まで登録できるようにする
        for i in range(2, 11):
            if f"image_{i}" in data:
                data["images"].append({"photo_path": data.pop(f"image_{i}")[0], "order": i})
            else:
                break

        serializer = ItemCreateSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            saved_item = Item.objects.get(id=serializer.data["id"])
            response_serializer = ItemSerializer(saved_item, context={"request": request})
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

    def update(self, request, *args, **kwargs):
        partial = self.request.query_params.get("partial", False)
        instance = self.get_object()
        print("partial: ", partial)
        print("keywargs: ", kwargs)

        if instance.listing_status != Item.ListingStatus.UNPURCHASED:
            return Response({"error": "売り切れた商品は編集できません。"}, status=status.HTTP_400_BAD_REQUEST)

        # request.dataを変更可能な辞書にコピー
        data = dict(request.data.lists())
        # Itemの作成に必要なキー
        keys_to_check = [
            "price",
            "name",
            "description",
            "condition",
            "writing_state",
            "receivable_campus",
        ]
        # キーが辞書に存在しないときエラーを返す
        for key in keys_to_check:
            if key not in data:
                if partial:
                    continue
                else:
                    return Response({"error": f"{key} が必要です"}, status=status.HTTP_400_BAD_REQUEST)
            data[key] = data[key][0]

        data["seller"] = request.user.id
        data["listing_status"] = instance.listing_status

        # 以下画像の処理
        data["images"] = []
        # partial == True のとき
        if partial:
            for i in range(1, 11):
                if f"image_{i}" in data:
                    data["images"].append({"photo_path": data.pop(f"image_{i}")[0], "order": i})

        # partial == False のとき
        else:
            if "image_1" not in data:
                return Response({"error": "写真が必須です。"}, status=status.HTTP_400_BAD_REQUEST)
            data["images"] = []
            data["images"].append({"photo_path": data.pop("image_1")[0], "order": 1})
            # 10枚まで登録できるようにする
            for i in range(2, 11):
                if f"image_{i}" in data:
                    data["images"].append({"photo_path": data.pop(f"image_{i}")[0], "order": i})
                else:
                    break

        serializer = ItemCreateSerializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        print("aaa")
        self.perform_update(serializer)

        updated_item = self.get_object()
        response_serializer = ItemSerializer(updated_item, context={"request": request})
        return Response(response_serializer.data)


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
