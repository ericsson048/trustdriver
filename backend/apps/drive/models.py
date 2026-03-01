import os
import uuid

from django.conf import settings
from django.db import models


def upload_node_file(instance: "Node", filename: str) -> str:
    _, extension = os.path.splitext(filename)
    return f"uploads/{instance.owner_id}/{uuid.uuid4()}{extension.lower()}"


class Node(models.Model):
    class NodeType(models.TextChoices):
        FILE = "file", "File"
        FOLDER = "folder", "Folder"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="nodes",
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="children",
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=16, choices=NodeType.choices)
    size = models.BigIntegerField(null=True, blank=True)
    mime_type = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to=upload_node_file, blank=True)
    share_token = models.UUIDField(unique=True, null=True, blank=True)
    is_shared = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["owner", "parent"]),
            models.Index(fields=["share_token", "is_shared"]),
        ]
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name} ({self.type})"
