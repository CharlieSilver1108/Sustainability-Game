# Generated by Django 5.0.1 on 2024-02-26 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0011_alter_multiplechoicetask_correct_answer'),
    ]

    operations = [
        migrations.AddField(
            model_name='multiplechoicetask',
            name='points',
            field=models.IntegerField(default=0),
        ),
    ]
