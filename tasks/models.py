from django.db import models

class Task_Type(models.Model):
    task_type = models.CharField(max_length=30)
    points = models.IntegerField(default=0)
    def __str__(self):
        return self.task_type

class Task(models.Model):
    name = models.CharField(max_length=30, default='Name')
    location = models.CharField(max_length=30, default='Location')
    description = models.CharField(max_length=200, default='description')
    task_type = models.ForeignKey(Task_Type, on_delete=models.CASCADE)
    answer = models.CharField(max_length=300, default='Answer')
    def __str__(self):
        return self.name