# Generated by Django 3.2.4 on 2021-07-05 10:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('francesubdivisions', '0029_auto_20210705_1201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='departement',
            name='insee',
            field=models.CharField(max_length=3, validators=[django.core.validators.RegexValidator('^([0-1]\\d|2[AB1-9]|[3-8]\\d|9[0-5]|97[12346])$')], verbose_name='identifiant Insee'),
        ),
    ]