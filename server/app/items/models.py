import uuid
from django.conf import settings
from django.db import models

from campuses.models import Campus


class Item(models.Model):
    class Meta:
        verse_name = "出品"

    ListingStatus = (("unpurchased", "未購入"), ("purchased", "購入後"), ("completed", "完了後"), ("canceled", "キャンセル後"))
    Condition = (("clean", "未使用"), ("used", "やや汚れや書き込みあり"), ("polluted", "汚れや書き込みあり"), ("terrible", "全体的に状態が悪い"))

    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    listing_stauts = models.CharField(choices=ListingStatus, default="unpurchased")
    price = models.PositiveIntegerField()
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    photo = models.ForeignKey(Image, on_delete=models.CASCADE)
    condition = models.CharField(choices=Condition)
    receivable_campus = models.ForeignKey(Campus, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# アップロード先のパス: <MEDIA_ROOT>/images/item/<出品者のユーザーID>/<ファイル名>
def get_item_image_path(instance, filename):
    return 'images/item/{0}/{1}'.format(instance.parent_item.seller.id, filename)


class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    parent_item = models.ForeignKey(Item, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=get_item_image_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)
