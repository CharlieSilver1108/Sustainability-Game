from django.db import models
from django.conf import settings

# ------- Luke START -------
class CarbonMonster(models.Model):
    monster_name = models.CharField(max_length=30)
    monster_type = models.CharField(max_length=30)
    initial_health_points = models.IntegerField(default=0)
    health_points = models.IntegerField(default=0)
    monster_sprite = models.ImageField(upload_to='pollution/', default='pollution/monster1.png')
    def __str__(self):
        return self.monster_name
    
class CarbonMonsterRelation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    monster = models.ForeignKey(CarbonMonster, on_delete=models.CASCADE)
    health_points = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return (self.user.username + self.monster.monster_name)

# ------- Luke END -------