from rest_framework import serializers
from .models import Item, Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"


# TODO: seller、read_only=Trueかも
class ItemSerializer(serializers.ModelSerializer):
    image_set = ImageSerializer(many=True)

    class Meta:
        model = Item
        fields = "__all__"

    def create(self, validated_data):
        validated_data["seller"] = self.context["request"].user
        validated_data["buyer"] = None
        validated_data["listing_status"] = Item.ListingStatus.UNPURCHASED

        images_data = self.context.get("image_data")
        item_insrance = Item.objects.create(**validated_data)
        for image_data in images_data:
            Image.objects.create(parent_item=item_insrance, **image_data)
        return item_insrance
