# Generated by Django 4.2.9 on 2024-03-15 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pollution', '0002_carbonmonster_monster_sprite'),
    ]

    operations = [
        migrations.AddField(
            model_name='carbonmonster',
            name='initial_health_points',
            field=models.IntegerField(default=0),
        ),
    ]