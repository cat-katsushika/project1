from rest_framework import serializers
from .models import Item, Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"


class ItemSerializer(serializers.ModelSerializer):
    seller = serializers.ReadOnlyField(source="seller.student_number")
    receivable_campus = serializers.ReadOnlyField(source="receivable_campus.campus")
    images = ImageSerializer(many=True, required=False)

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
        validated_data["seller"] = self.context["request"].user
        validated_data["buyer"] = None
        validated_data["listing_status"] = Item.ListingStatus.UNPURCHASED

        images_data = self.context.get("images")
        item = Item.objects.create(**validated_data)
        self.create_images(item, images_data)
        return item

    def create_images(self, item, images_data):
        for index, image_data in enumerate(images_data, start=1):
            Image.objects.create(parent_item=item, order=index, **image_data)

    def update(self, instance, validated_data):
        images_data = self.context.get("images")
        item = super().update(instance, validated_data)
        self.update_images(item, images_data)
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
