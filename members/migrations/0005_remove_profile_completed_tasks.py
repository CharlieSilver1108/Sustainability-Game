# Generated by Django 5.0.2 on 2024-02-24 15:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0004_alter_profile_completed_tasks'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='completed_tasks',
        ),
    ]