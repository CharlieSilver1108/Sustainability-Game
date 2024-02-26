from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from tasks.models import Task, Task_Type

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    taskOne = models.ForeignKey(Task, related_name='taskOne', on_delete=models.CASCADE, null=True, blank=True)
    taskTwo = models.ForeignKey(Task, related_name='taskTwo', on_delete=models.CASCADE, null=True, blank=True)
    taskThree = models.ForeignKey(Task, related_name='taskThree', on_delete=models.CASCADE, null=True, blank=True)
    points = models.IntegerField(default=0)
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='default.jpg')
    
    def __str__(self):
        return str(self.user)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()