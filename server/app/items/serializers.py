from rest_framework import serializers

from .models import Item, Image
from PIL import Image as PILImage
import io


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ("order", "photo_path")
        extra_kwargs = {"order": {"required": False}}


class ItemSerializer(serializers.ModelSerializer):
    seller = serializers.ReadOnlyField(source="seller.email", default=serializers.CurrentUserDefault())
    receivable_campus = serializers.CharField(source="receivable_campus.campus")
    images = ImageSerializer(many=True)
    is_liked_by_current_user = serializers.SerializerMethodField()

    def get_buyer(self, obj):
        if obj.buyer:
            return obj.buyer.email
        return None

    def get_is_liked_by_current_user(self, obj):
        user = self.context["request"].user
        if user.is_authenticated:
            return obj.liked_by.filter(user=user).exists()
        return False

    class Meta:
        model = Item
        fields = "__all__"

    def validate_images(self, images_data):
        if len(images_data) < 1:
            raise serializers.ValidationError("写真は必須です。")
        elif len(images_data) > 10:
            raise serializers.ValidationError("写真は10枚までしか登録できません。")
        return images_data

    def create(self, validated_data):
        validated_data["buyer"] = None
        validated_data["listing_status"] = Item.ListingStatus.UNPURCHASED

        images_data = validated_data.pop("images")
        item = Item.objects.create(**validated_data)
        self.create_images(item, images_data)
        self.process_images(item)
        return item

    def create_images(self, item, images_data):
        for index, image_data in enumerate(images_data, start=1):
            Image.objects.create(parent_item=item, order=index, **image_data)

    def update(self, instance, validated_data):
        images_data = validated_data.pop("images")
        item = super().update(instance, validated_data)
        self.update_images(item, images_data)
        self.process_images(item)
        return instance

    def update_images(self, item, images_data):
        existing_images = item.images.all()

        for index, image_data in enumerate(images_data, start=1):
            image_id = image_data.get("id", None)
            # 更新
            if image_id is not None:
                image = existing_images.get(id=image_id)
                image.order = index
                image.save()
            # 新規作成
            else:
                Image.objects.create(parent_item=item, order=index, **image_data)

        # 削除
        image_data_ids = [image_data.get("id") for image_data in images_data]
        for image in existing_images:
            if image.id not in image_data_ids:
                image.delete()

    def process_images(self, item):
        for image in item.images.all():
            self.convert_to_jpeg(image)

    def convert_to_jpeg(self, image):
        if image.format != "JPEG":
            try:
                # 画像を開いてRGB形式に変換
                img = PILImage.open(image.photo_path)
                img = img.convert("RGB")
                # 画像をJPEG形式で保存するためのバッファを作成
                buffer = io.BytesIO()
                img.save(buffer, format="JPEG")
                # バッファの内容をファイルオブジェクトに書き込む
                image.photo_path.save(image.photo_path.name, content=ContentFile(buffer.getvalue()), save=False)
            except Exception:
                raise serializers.ValidationError("画像の変換に失敗しました。")
