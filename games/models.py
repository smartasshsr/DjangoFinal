from django.db import models
from django.conf import settings

# Create your models here.
# [미션] 자유롭게 코드 작성
# [미션] 필요한 필드가 있다면 추가하기
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
