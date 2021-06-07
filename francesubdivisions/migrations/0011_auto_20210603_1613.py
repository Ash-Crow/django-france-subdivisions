# Generated by Django 3.2.4 on 2021-06-03 14:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('francesubdivisions', '0010_auto_20210601_1557'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataSource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='date de création')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='date de modification')),
            ],
            options={
                'ordering': ['created_at'],
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='commune',
            name='created',
        ),
        migrations.RemoveField(
            model_name='datayear',
            name='created',
        ),
        migrations.RemoveField(
            model_name='departement',
            name='created',
        ),
        migrations.RemoveField(
            model_name='epci',
            name='created',
        ),
        migrations.RemoveField(
            model_name='metadata',
            name='created',
        ),
        migrations.RemoveField(
            model_name='region',
            name='created',
        ),
        migrations.AddField(
            model_name='commune',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='date de création'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='commune',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='date de modification'),
        ),
        migrations.AddField(
            model_name='datayear',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='date de création'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='datayear',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='date de modification'),
        ),
        migrations.AddField(
            model_name='departement',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='date de création'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='departement',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='date de modification'),
        ),
        migrations.AddField(
            model_name='epci',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='date de création'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='epci',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='date de modification'),
        ),
        migrations.AddField(
            model_name='metadata',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='date de création'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='metadata',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='date de modification'),
        ),
        migrations.AddField(
            model_name='region',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='date de création'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='region',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='date de modification'),
        ),
    ]