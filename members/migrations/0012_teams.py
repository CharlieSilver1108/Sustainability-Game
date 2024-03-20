from django.db import migrations
from django.contrib.auth.models import Group

def create_teams(apps, schema_editor):
    # Create the teams if they don't exist
    Group.objects.get_or_create(name='Eco Pioneers')
    Group.objects.get_or_create(name='Green Guardians')
    Group.objects.get_or_create(name='Recycle Rangers')

class Migration(migrations.Migration):

    dependencies = [
        ('members', '0011_profile_highest_position'),
    ]

    operations = [
        migrations.RunPython(create_teams),
    ]