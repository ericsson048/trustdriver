import django.utils.timezone
import uuid

from django.db import migrations, models


def mark_existing_users_verified(apps, schema_editor):
    User = apps.get_model("accounts", "User")
    User.objects.filter(email_verified=False).update(email_verified=True)


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0002_alter_user_managers_user_is_superuser_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="email_verified",
            field=models.BooleanField(default=True),
        ),
        migrations.RunPython(mark_existing_users_verified, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="user",
            name="email_verified",
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name="EmailVerificationToken",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("token", models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ("expires_at", models.DateTimeField()),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "user",
                    models.OneToOneField(on_delete=models.deletion.CASCADE, related_name="email_verification_token", to="accounts.user"),
                ),
            ],
        ),
    ]
