# Generated by Django 3.1.2 on 2020-11-20 16:07
from django.db import migrations
from django.contrib.postgres.operations import UnaccentExtension


class Migration(migrations.Migration):

    dependencies = [
        ("francesubdivisions", "0003_auto_20201103_1412"),
    ]

    operations = [UnaccentExtension()]