# Generated by Django 5.0.1 on 2024-02-26 17:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0006_alter_multiplechoicetask_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='multiplechoicetask',
            name='name',
        ),
    ]
