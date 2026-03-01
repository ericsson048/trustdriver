import apps.drive.models
import uuid

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Node",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=255)),
                ("type", models.CharField(choices=[("file", "File"), ("folder", "Folder")], max_length=16)),
                ("size", models.BigIntegerField(blank=True, null=True)),
                ("mime_type", models.CharField(blank=True, max_length=255)),
                ("file", models.FileField(blank=True, upload_to=apps.drive.models.upload_node_file)),
                ("share_token", models.UUIDField(blank=True, null=True, unique=True)),
                ("is_shared", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "owner",
                    models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="nodes", to=settings.AUTH_USER_MODEL),
                ),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=models.deletion.CASCADE,
                        related_name="children",
                        to="drive.node",
                    ),
                ),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.AddIndex(
            model_name="node",
            index=models.Index(fields=["owner", "parent"], name="drive_node_owner_i_7b1528_idx"),
        ),
        migrations.AddIndex(
            model_name="node",
            index=models.Index(fields=["share_token", "is_shared"], name="drive_node_share_t_c850f2_idx"),
        ),
    ]
