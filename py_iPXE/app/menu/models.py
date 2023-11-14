#models.py

from typing import Any
from django.db import models

# Create your models here.

class iPXE_Menu_item(models.Model):
    item_name = models.CharField(max_length=30, primary_key=True)
    item_contents = models.TextField()


class iPXE_Menu(models.Model):
    title = models.CharField(max_length=30, primary_key=True)
    steps = models.ManyToManyField(iPXE_Menu_item, null=True)

class Wimager_Menus(iPXE_Menu):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
    # add iPXE menu fields

class Watched_File(models.Model):
    file_name = models.TextField()
    file_path = models.TextField()
    last_edited = models.DateTimeField()
class Watched_Directory(models.Model):
    absolute_path = models.TextField()
    files = models.ManyToManyField(Watched_File)

class Tracked_Directories(models.Model):
    directory = models.ManyToManyField(Watched_Directory)
    last_updated = models.DateTimeField()

