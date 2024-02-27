# Generated by Django 5.0.1 on 2024-02-27 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0012_multiplechoicetask_points'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonBasedCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=4)),
                ('name', models.CharField(max_length=30)),
                ('location', models.CharField(max_length=30)),
                ('expertise', models.CharField(max_length=30)),
            ],
        ),
        migrations.AlterField(
            model_name='multiplechoicetask',
            name='description',
            field=models.CharField(blank=True, default='This is a multiple choice task', max_length=200),
        ),
        migrations.AlterField(
            model_name='multiplechoicetask',
            name='location',
            field=models.CharField(blank=True, default='forum', max_length=30),
        ),
        migrations.AlterField(
            model_name='multiplechoicetask',
            name='points',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
