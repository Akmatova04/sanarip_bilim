# Generated by Django 5.2 on 2025-04-17 21:31

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Аталышы')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Сүрөттөмөсү')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Түзүлгөн күнү')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Жаңыланган күнү')),
            ],
            options={
                'verbose_name': 'Курс',
                'verbose_name_plural': 'Курстар',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Аталышы')),
                ('link', models.URLField(max_length=500, verbose_name='Шилтеме')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Сүрөттөмөсү')),
                ('added_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Кошулган күнү')),
            ],
            options={
                'verbose_name': 'Ресурс',
                'verbose_name_plural': 'Ресурстар',
                'ordering': ['-added_at'],
            },
        ),
    ]
