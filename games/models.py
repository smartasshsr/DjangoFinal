from django.db import models
from django.conf import settings

# Create your models here.
class Weapon(models.Model):
    name = models.CharField(max_length=20)
    power = models.IntegerField()

    def __str__(self):
        return self.name

class Character(models.Model):
    nickname = models.CharField(max_length=20)
    weapon = models.ForeignKey(Weapon, on_delete=models.CASCADE, related_name='character_list', null=True, blank=True)
    coin = models.BigIntegerField(default = 0)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='character', null=True, blank=True)

    def __str__(self):
        return self.nickname

class Enemy(models.Model):
    name = models.CharField(max_length=20)
    hp = models.IntegerField()

    def __str__(self):
        return self.name
