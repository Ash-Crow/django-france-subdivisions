# Generated by Django 3.2.4 on 2021-07-02 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('francesubdivisions', '0020_auto_20210702_1106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datayear',
            name='year',
            field=models.PositiveSmallIntegerField(unique=True),
        ),
    ]
