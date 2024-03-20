# Generated by Django 4.2.9 on 2024-03-20 15:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pollution', '0003_carbonmonster_initial_health_points'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarbonMonsterRelation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('health_points', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('monster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pollution.carbonmonster')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
