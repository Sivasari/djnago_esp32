# Generated by Django 5.1.6 on 2025-03-07 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fire_monitor', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='firesensor',
            name='timestamp',
        ),
        migrations.AddField(
            model_name='firesensor',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
