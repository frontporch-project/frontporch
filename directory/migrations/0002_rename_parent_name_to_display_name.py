from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("directory", "0001_initial"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="parent",
            name="unique_parent_name_per_family",
        ),
        migrations.RenameField(
            model_name="parent",
            old_name="name",
            new_name="display_name",
        ),
        migrations.AlterModelOptions(
            name="parent",
            options={"ordering": ["family__name", "display_name"]},
        ),
        migrations.AddConstraint(
            model_name="parent",
            constraint=models.UniqueConstraint(
                fields=("family", "display_name"),
                name="unique_parent_display_name_per_family",
            ),
        ),
    ]
