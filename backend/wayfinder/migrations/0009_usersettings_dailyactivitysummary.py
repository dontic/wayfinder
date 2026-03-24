from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("wayfinder", "0008_alter_location_device_id_alter_visit_device_id"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="UserSettings",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("home_timezone", models.CharField(default="UTC", max_length=63)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="wayfinder_settings",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "user settings",
            },
        ),
        migrations.CreateModel(
            name="DailyActivitySummary",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField()),
                ("timezone", models.CharField(max_length=63)),
                ("location_count", models.IntegerField(default=0)),
                ("visit_count", models.IntegerField(default=0)),
                ("computed_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": ["date"],
                "unique_together": {("date", "timezone")},
            },
        ),
    ]
