import os
import uuid

from django.conf import settings
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from campuses.models import Campus


class Item(models.Model):
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

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sell_item")
    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name="buy_item"
    )
    # MEMO: キャンセル済みは未時購入で吸収してもいいかも
    listing_status = models.CharField(max_length=11, choices=ListingStatus.choices, default=ListingStatus.UNPURCHASED)
    price = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=50)
    # MEMO: Textにする？文字数制限どうする？
    description = models.CharField(max_length=255)
    condition = models.CharField(max_length=7, choices=Condition.choices)
    writing_state = models.CharField(max_length=6, choices=WritingState.choices)
    receivable_campus = models.ForeignKey(Campus, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    # MEMO: いるかなと思って追加しといた。いらなかったら消す。
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# MEMO: URLにユーザーIDいらないかも
# アップロード先のパス: <MEDIA_ROOT>/images/items/<出品者のユーザーID>/<ファイル名>
def get_item_image_path(instance, filename):
    return "images/items/{0}/{1}".format(instance.parent_item.seller.id, filename)


class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    parent_item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="images")
    photo_path = models.ImageField(upload_to=get_item_image_path)
    order = models.PositiveSmallIntegerField()
    uploaded_at = models.DateTimeField(auto_now_add=True)


# Imageモデルのオブジェクトが削除される前に、関連する画像ファイルを削除する
@receiver(pre_delete, sender=Image)
def delete_image_files(sender, instance, **kwargs):
    if instance.photo_path:
        if os.path.isfile(instance.photo_path.path):
            os.remove(instance.photo_path.path)


class Like(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="liked_by")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
