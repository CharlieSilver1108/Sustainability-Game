# Generated by Django 4.2.9 on 2024-03-14 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0009_badge_useractivity_profilebadgerelation_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='pointsToAttack',
            field=models.IntegerField(default=0),
        ),
    ]
