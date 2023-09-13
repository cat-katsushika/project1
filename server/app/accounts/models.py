import uuid

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("メールアドレスは必須です")

        email = self.normalize_email(email)
        email = email.lower()
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(
        verbose_name="ユーザーID",
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    email = models.EmailField(
        verbose_name="メールアドレス",
        max_length=350,
        unique=True,
    )
    is_staff = models.BooleanField(
        verbose_name="管理サイトアクセス権限フラグ",
        default=False,
    )
    is_active = models.BooleanField(
        verbose_name="アカウント有効フラグ",
        default=False,
    )
    created_at = models.DateTimeField(
        verbose_name="作成日",
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name="更新日",
        auto_now=True,
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"

    class Meta:
        verbose_name = "ユーザー"

    def __str__(self):
        return self.email
