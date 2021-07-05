# Generated by Django 3.2.4 on 2021-07-05 15:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('francesubdivisions', '0031_alter_region_siren'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commune',
            name='insee',
            field=models.CharField(max_length=5, validators=[django.core.validators.RegexValidator('^\\d[0-9AB][0-9P]\\d\\d$')], verbose_name='identifiant Insee'),
        ),
    ]
