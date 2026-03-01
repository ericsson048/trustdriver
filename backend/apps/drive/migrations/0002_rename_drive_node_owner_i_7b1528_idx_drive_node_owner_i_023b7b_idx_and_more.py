from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("drive", "0001_initial"),
    ]

    operations = [
        migrations.RenameIndex(
            model_name="node",
            new_name="drive_node_owner_i_023b7b_idx",
            old_name="drive_node_owner_i_7b1528_idx",
        ),
        migrations.RenameIndex(
            model_name="node",
            new_name="drive_node_share_t_0e69c5_idx",
            old_name="drive_node_share_t_c850f2_idx",
        ),
    ]
