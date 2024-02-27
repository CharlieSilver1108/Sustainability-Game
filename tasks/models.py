from django.db import models

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
    description = models.CharField(max_length=200)
    task_type = models.ForeignKey(Task_Type, on_delete=models.CASCADE)
    answer = models.CharField(max_length=300)
    def __str__(self):
        return self.name

# ------- END -------