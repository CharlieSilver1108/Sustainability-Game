# Generated by Django 5.0.2 on 2024-03-21 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0024_multiplechoicechallenge_qr_code_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='multiplechoicechallenge',
            name='question',
            field=models.CharField(max_length=2000),
        ),
    ]
