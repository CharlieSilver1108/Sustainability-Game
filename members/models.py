from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from tasks.models import Task, Task_Type
from django.utils import timezone
from datetime import timedelta
import logging

# ------- Luke START (+ Charlie, Liam, Greg) -------

# the Profile class is an extension of the User class that is provided by Django
# the class holds the current tasks a user has, as well as the number of points that the user has 
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    taskOne = models.ForeignKey(Task, related_name='taskOne', on_delete=models.CASCADE, null=True, blank=True)
    taskTwo = models.ForeignKey(Task, related_name='taskTwo', on_delete=models.CASCADE, null=True, blank=True)
    taskThree = models.ForeignKey(Task, related_name='taskThree', on_delete=models.CASCADE, null=True, blank=True)
    points = models.IntegerField(default=0)
    pointsToAttack = models.IntegerField(default=0)
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='profile_pictures/default.png')  # -Liam-
    bio = models.TextField(max_length=500, null=True, blank=True)   # -Liam-
    pronouns = models.CharField(max_length=10 ,null=True, blank=True)   # -Charlie-
    badges = models.ManyToManyField('Badge', through='ProfileBadgeRelation') # -Greg-
    highest_position = models.IntegerField(null=True, blank=True) # -Greg-
    team = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True) # -Greg-
    challenges_completed = models.IntegerField(default=0) # -Greg-
    monsters_defeated = models.IntegerField(default=0) # -Greg-
    tree_grown = models.BooleanField(default=False) # -Greg-
    

    def check_and_assign_badges(self):
        # Assings earned badges to the profile if the criteria is met
        badges = Badge.objects.all() # Get all badges
        for badge in badges: 
            # If the badge is earned and not already assigned to the profile, assign it
            if badge.is_earned_by(self):
                self.badges.add(badge)
                self.save()
    
    def __str__(self):
        return str(self.user)
    
 # This model represents a badge that a user can earn. Each badge has a unique name, a description, 
 # and a criteria. The `is_earned_by` method checks if a profile has earned the badge by calling a 
 # rule function associated with the badge's name. Rule functions should be named 'rule_{badge_name}' 
 # and return True if the profile has earned the badge, and False otherwise.
class Badge(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=200)
    criteria = models.CharField(max_length=200)
    image = models.ImageField(upload_to='badges/', null=True)

    def __str__(self):
        return self.name

    def is_earned_by(self, profile):
        # Call the rule function associated with this badge
        rule_function = getattr(self, f'rule_{self.name}', None)
        if rule_function is not None:
            result = rule_function(profile)
            return result
        return False
    
    ## Badge rule functions

    def rule_500_points(self, profile): # When creating this the badge it must be called '500_points'
        # Check if the profile has at least 500 points
        return profile.points >= 500

    def rule_1000_points(self, profile): # When creating this the badge it must be called '500_points'
        # Check if the profile has at least 500 points
        return profile.points >= 1000

    def rule_top_10(self, profile):
        # Check if the profile has ever been in the top 10
        return profile.highest_position is not None and profile.highest_position <= 10
    
    def rule_sustainability_star(self, profile):
        # Check if the user has completed at least sustainability tasks
        return profile.challenges_completed >= 3
    
    def rule_monster_hunter(self, profile):
        # Check if the user has defeated at least 5 monsters
        return profile.monsters_defeated >= 5

    def rule_tree_hugger(self, profile):  # When creating this badge it must be called 'tree_hugger'
        # Check if the tree has been grown at least once
        return profile.tree_grown

 # This model represents the relationship between a Profile and a Badge. 
 # It has a foreign key to both Profile and Badge, indicating which profile 
 # has earned which badge. The `created_at` field records when the badge was 
 # awarded to the profile.
class ProfileBadgeRelation(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.profile} - {self.badge}"
    
# this receiver function creates a new profile whenever a new user has been created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
        profile.save()
        
# this receiver function updates the profile of the user whenever a change is made
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    instance.profile.check_and_assign_badges()

# ------- Luke END -------