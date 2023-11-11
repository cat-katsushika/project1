from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class CommentCreateTest(APITestCase):
    fixtures = [
        "accounts/fixtures/users.yaml",
        "notifications/fixtures/notifications.yaml",
    ]

    def setUp(self):
        url = reverse("login")  # JWTトークン取得エンドポイント
        data = {"email": "test1@example.com", "password": "test"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data["access"]  # JWTアクセストークンを取得
        self.client.cookies["access_token"] = token

    def test_get_notification_list(self):
        """
        通知リストを取得するテスト
        """
        url = reverse("notification-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
