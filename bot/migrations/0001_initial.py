# Generated by Django 5.1.3 on 2024-12-02 03:10

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CheckinRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=100)),
                ('checkin_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('checkout_time', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BreakRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('reason', models.TextField()),
                ('checkin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='breaks', to='bot.checkinrecord')),
            ],
        ),
        migrations.CreateModel(
            name='TaskRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.TextField()),
                ('completed', models.BooleanField(default=False)),
                ('checkin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='bot.checkinrecord')),
            ],
        ),
    ]
