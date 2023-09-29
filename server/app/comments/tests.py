from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model


from items.models import Item

User = get_user_model()


class CommentCreateTest(TestCase):
    fixtures = [
        "accounts/fixtures/data.json",
        "campuses/fixtures/data.json",
        "items/fixtures/data.json",
    ]

    """
    コメント作成機能のテストクラス。

    属性:
    - client: APIリクエストを行うためのAPIClientのインスタンス。
    - user: テストのために作成されたテストユーザー。
    - item: テストのために作成されたサンプルアイテム。
    - comment_data: テストで使用されるサンプルのコメントデータ。
    - url: コメント作成のためのAPIエンドポイントのURL。
    """

    def setUp(self):
        """
        テストケースのセットアップメソッド。テストユーザーとアイテムを作成し、それで認証します。
        また、APIエンドポイントのURLとサンプルのコメントデータを設定します。
        """
        self.client = APIClient()
        self.user = User.objects.create_user(email="test@example.com", password="testpass")
        self.item = Item.objects.get(pk="6fd2f1142af84d4586586d64324be72d")
        self.client.force_authenticate(user=self.user)
        self.comment_data = {"comment": "テストコメント", "item_id": self.item.id}
        self.url = reverse("comment-create")

    def test_create_comment(self):
        """
        アイテムIDを指定して、コメントの作成APIエンドポイントにPOSTリクエストを行い、
        コメントが正常にアイテムに関連付けて作成されることを確認するテストメソッド。
        """
        response = self.client.post(self.url, self.comment_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["comment"], self.comment_data["comment"])
        self.assertEqual(response.data["user"], self.user.id)
        self.assertEqual(response.data["item_id"], self.item.id)
