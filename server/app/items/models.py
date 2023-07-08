import uuid

from django.conf import settings
from django.db import models

from campuses.models import Campus


class Item(models.Model):
    class Meta:
        verbose_name = "出品"

    class ListingStatus(models.TextChoices):
        UNPURCHASED = "unpurchased", "未購入"
        PURCHASED = "purchased", "購入済み"
        COMPLETED = "completed", "取引完了"
        CANCELED = "canceled", "キャンセル済み"

    class Condition(models.TextChoices):
        NEW = "new", "未使用"
        FINE = "fine", "目立った傷や汚れなし"
        USED = "used", "使用感あり"
        DAMAGED = "damaged", "破損あり"

    class WritingState(models.TextChoices):
        NONE = "none", "全くない"
        LITTLE = "little", "少しある"
        LOT = "lot", "かなりある"

    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sells")
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="buys")
    listing_stauts = models.CharField(max_length=30, choices=ListingStatus.choices, default=ListingStatus.UNPURCHASED)
    price = models.PositiveIntegerField()
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    condition = models.CharField(max_length=30, choices=Condition.choices)
    writing_state = models.CharField(max_length=30, choices=WritingState.choices)
    receivable_campus = models.ForeignKey(Campus, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# アップロード先のパス: <MEDIA_ROOT>/images/item/<出品者のユーザーID>/<ファイル名>
def get_item_image_path(instance, filename):
    return "images/item/{0}/{1}".format(instance.parent_item.seller.id, filename)


class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    parent_item = models.ForeignKey(Item, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=get_item_image_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)
