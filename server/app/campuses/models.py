from uuid import uuid4

from django.db import models


class University(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=100)


class Campus(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    campus = models.CharField(max_length=100)
