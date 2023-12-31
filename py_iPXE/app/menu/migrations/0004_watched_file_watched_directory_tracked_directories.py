# Generated by Django 4.2.7 on 2023-11-14 22:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("menu", "0003_wimager_menus_alter_ipxe_menu_steps"),
    ]

    operations = [
        migrations.CreateModel(
            name="Watched_File",
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
                ("file_name", models.TextField()),
                ("file_path", models.TextField()),
                ("last_edited", models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name="Watched_Directory",
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
                ("absolute_path", models.TextField()),
                ("files", models.ManyToManyField(to="menu.watched_file")),
            ],
        ),
        migrations.CreateModel(
            name="Tracked_Directories",
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
                ("last_updated", models.DateTimeField()),
                ("directory", models.ManyToManyField(to="menu.watched_directory")),
            ],
        ),
    ]
