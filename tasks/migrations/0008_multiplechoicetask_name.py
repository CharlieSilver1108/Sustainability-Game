# Generated by Django 5.0.1 on 2024-02-26 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0007_remove_multiplechoicetask_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='multiplechoicetask',
            name='name',
            field=models.CharField(default='Name', max_length=30),
        ),
    ]
