# Generated by Django 5.2 on 2025-04-18 00:10

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_contactmessage'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='Аталышы')),
                ('content', models.TextField(verbose_name='Мазмуну')),
                ('published_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Жарыяланган күнү')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Автору')),
            ],
            options={
                'verbose_name': 'Блог Посту',
                'verbose_name_plural': 'Блог Посттору',
                'ordering': ['-published_date'],
            },
        ),
    ]
