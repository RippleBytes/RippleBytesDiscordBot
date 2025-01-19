# Generated by Django 5.1.3 on 2025-01-16 06:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskrecord',
            name='show',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='taskrecord',
            name='checkin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='bot.checkinrecord'),
        ),
        migrations.AlterField(
            model_name='taskrecord',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
