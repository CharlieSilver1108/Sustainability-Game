from django.db import models

# ------- Luke START -------
class CarbonMonster(models.Model):
    monster_name = models.CharField(max_length=30)
    monster_type = models.CharField(max_length=30)
    initial_health_points = models.IntegerField(default=0)
    health_points = models.IntegerField(default=0)
    monster_sprite = models.ImageField(upload_to='pollution/', default='pollution/test_monster1')
    def __str__(self):
        return self.monster_name
# ------- Luke END -------