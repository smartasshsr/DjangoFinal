from django.contrib import admin
from .models import Weapon, Character, Enemy

# Register your models here.
admin.site.register(Weapon)
admin.site.register(Character)
admin.site.register(Enemy)
