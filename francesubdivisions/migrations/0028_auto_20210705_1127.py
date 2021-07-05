# Generated by Django 3.2.4 on 2021-07-05 09:27

from django.db import migrations, models
import francesubdivisions.services.validators


class Migration(migrations.Migration):

    dependencies = [
        ('francesubdivisions', '0027_alter_epci_siren'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commune',
            name='siren',
            field=models.CharField(blank=True, max_length=9, validators=[francesubdivisions.services.validators.validate_siren], verbose_name='numéro Siren'),
        ),
        migrations.AlterField(
            model_name='departement',
            name='siren',
            field=models.CharField(blank=True, max_length=9, validators=[francesubdivisions.services.validators.validate_siren], verbose_name='numéro Siren'),
        ),
        migrations.AlterField(
            model_name='epci',
            name='siren',
            field=models.CharField(max_length=9, validators=[francesubdivisions.services.validators.validate_siren], verbose_name='numéro Siren'),
        ),
        migrations.AlterField(
            model_name='region',
            name='siren',
            field=models.CharField(blank=True, max_length=9, validators=[francesubdivisions.services.validators.validate_siren], verbose_name='numéro Siren'),
        ),
    ]