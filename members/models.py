from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from tasks.models import Task, Task_Type

# ------- Luke START (+ Charlie, Liam) -------

# the Profile class is an extension of the User class that is provided by Django
# the class holds the current tasks a user has, as well as the number of points that the user has 
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    taskOne = models.ForeignKey(Task, related_name='taskOne', on_delete=models.CASCADE, null=True, blank=True)
    taskTwo = models.ForeignKey(Task, related_name='taskTwo', on_delete=models.CASCADE, null=True, blank=True)
    taskThree = models.ForeignKey(Task, related_name='taskThree', on_delete=models.CASCADE, null=True, blank=True)
    points = models.IntegerField(default=0)
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='profile_pictures/default.png')  # -Liam-
    bio = models.TextField(max_length=500, null=True, blank=True)   # -Liam-
    pronouns = models.CharField(max_length=10 ,null=True, blank=True)   # -Charlie-
    
    def __str__(self):
        return str(self.user)

# this receiver function creates a new profile whenever a new user has been created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
# this receiver function updates the profile of the user whenever a change is made
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# ------- Luke END -------