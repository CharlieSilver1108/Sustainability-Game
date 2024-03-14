from django.db import models

class CarbonMonster(models.Model):
    monster_name = models.CharField(max_length=30)
    monster_type = models.CharField(max_length=30)
    health_points = models.IntegerField(default=0)
    def __str__(self):
        return self.monster_name