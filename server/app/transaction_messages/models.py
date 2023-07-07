from uuid import uuid4

from django.conf import settings
from django.db import models
from django.utils import timezone


class Message(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)