# Generated by Django 3.2.4 on 2021-07-05 10:01

import django.core.validators
from django.db import migrations, models
import francesubdivisions.services.validators


class Migration(migrations.Migration):

    dependencies = [
        ('francesubdivisions', '0028_auto_20210705_1127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='departement',
            name='siren',
            field=models.CharField(blank=True, max_length=9, null=True, validators=[francesubdivisions.services.validators.validate_siren], verbose_name='numéro Siren'),
        ),
        migrations.AlterField(
            model_name='region',
            name='insee',
            field=models.CharField(max_length=2, validators=[django.core.validators.RegexValidator('^\\d\\d$')], verbose_name='identifiant Insee'),
        ),
    ]