# Generated by Django 3.2.4 on 2021-06-09 13:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('francesubdivisions', '0017_alter_regiondata_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='DepartementData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='date de création')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='date de modification')),
                ('datacode', models.CharField(max_length=255, verbose_name='code')),
                ('value', models.CharField(blank=True, max_length=255, null=True, verbose_name='valeur')),
                ('datatype', models.CharField(blank=True, max_length=255, null=True, verbose_name='type')),
            ],
            options={
                'verbose_name': 'donnée département',
                'verbose_name_plural': 'données département',
            },
        ),
        migrations.RemoveConstraint(
            model_name='regiondata',
            name='unique metadata point',
        ),
        migrations.AddConstraint(
            model_name='regiondata',
            constraint=models.UniqueConstraint(fields=('region', 'year', 'datacode'), name='unique region data'),
        ),
        migrations.AddField(
            model_name='departementdata',
            name='departement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='francesubdivisions.departement', verbose_name='département'),
        ),
        migrations.AddField(
            model_name='departementdata',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='francesubdivisions.datasource', verbose_name='source'),
        ),
        migrations.AddField(
            model_name='departementdata',
            name='year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='francesubdivisions.datayear', verbose_name='millésime'),
        ),
        migrations.AddConstraint(
            model_name='departementdata',
            constraint=models.UniqueConstraint(fields=('departement', 'year', 'datacode'), name='unique departement data'),
        ),
    ]
