# Generated by Django 3.2.4 on 2021-06-09 10:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('francesubdivisions', '0016_alter_regiondata_datacode'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='regiondata',
            options={'verbose_name': 'donnée région', 'verbose_name_plural': 'données région'},
        ),
    ]
