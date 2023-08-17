from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import serializers
from .models import Item, Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"


class ItemSerializer(WritableNestedModelSerializer):
    images = ImageSerializer(many=True)

    class Meta:
        model = Item
        fields = "__all__"

    def create(self, validated_data):
        validated_data["seller"] = self.context["request"].user
        validated_data["buyer"] = None
        validated_data["listing_status"] = Item.ListingStatus.UNPURCHASED

        images_data = validated_data.pop("images", [])  # images データを一旦取り出す

        item = Item.objects.create(**validated_data)

        for image_data in images_data:
            Image.objects.create(parent_item=item, **image_data)

        return item
