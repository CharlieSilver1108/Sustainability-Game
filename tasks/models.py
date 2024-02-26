from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Task_Type(models.Model):
    task_type = models.CharField(max_length=30)
    points = models.IntegerField(default=0)
    def __str__(self):
        return self.task_type

class Task(models.Model):
    name = models.CharField(max_length=30, default='Name')
    location = models.CharField(max_length=30, default='Location')
    description = models.CharField(max_length=200, default='Description')
    task_type = models.ForeignKey(Task_Type, on_delete=models.CASCADE)
    answer = models.CharField(max_length=300, default='Answer')
    def __str__(self):
        return self.name
    

class MultipleChoiceTask(models.Model):
    code = models.CharField(max_length=30)
    location = models.CharField(max_length=30)
    description = models.CharField(max_length=200, null=True, blank=True)
    question = models.CharField(max_length=300)
    choice1 = models.CharField(max_length=30)
    choice2 = models.CharField(max_length=30)
    choice3 = models.CharField(max_length=30)
    choice4 = models.CharField(max_length=30)
    correct_answer = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)])
    def __str__(self):
        return self.code