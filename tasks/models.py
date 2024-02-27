from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings

# ------- CODING BY LUKE HALES -------

# creates the task type model, which holds the types of tasks that will be used as well as the number of points for each task type
class Task_Type(models.Model):
    task_type = models.CharField(max_length=30)
    points = models.IntegerField(default=0)
    def __str__(self):
        return self.task_type

# creates the task model which holds the name, description, an input to complete the task, and contains a foreign key which links it to a task type
class Task(models.Model):
    name = models.CharField(max_length=30)
    location = models.CharField(max_length=30, default='Location')
    description = models.CharField(max_length=200)
    task_type = models.ForeignKey(Task_Type, on_delete=models.CASCADE)
    answer = models.CharField(max_length=300)
    def __str__(self):
        return self.name

# ------- END -------

class MultipleChoiceTask(models.Model):
    code = models.CharField(max_length=30)
    location = models.CharField(max_length=30, default = 'forum', blank = True)
    description = models.CharField(max_length=200, default = 'This is a multiple choice task', blank = True)
    question = models.CharField(max_length=300)
    choice1 = models.CharField(max_length=30)
    choice2 = models.CharField(max_length=30)
    choice3 = models.CharField(max_length=30)
    choice4 = models.CharField(max_length=30)
    correct_answer = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)])
    points = models.IntegerField(default=0, null=True, blank=True)
    def __str__(self):
        return self.code
    
class PersonBasedCode(models.Model):
    # 4 digit code
    code = models.CharField(max_length=4)
    # name of the person, where they can be found and their area of expertise
    name = models.CharField(max_length=30)
    location = models.CharField(max_length=30)
    expertise = models.CharField(max_length=30)
    points = models.IntegerField(default=0)
    
class LocationBasedTask(models.Model):
    
    longitude = models.FloatField()
    latitude = models.FloatField()
    
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=200)
    points = models.IntegerField(default=0)
    
# currently have a join table for each one, may be able to create an abstract class to handle this
    
# join table between the user and the person based code so we can track what codes they've used/people visited
class UserCodeRelation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    person_based_code = models.ForeignKey(PersonBasedCode, on_delete=models.CASCADE)
    # You can add a timestamp here if you want to record when the code was added
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.person_based_code}"
    
# join table between the user the location based tasks that they have completed
class UserLocationRelation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    location_based_task = models.ForeignKey(LocationBasedTask, on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user} - {self.location_based_task}"