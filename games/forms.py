from django import forms
from .models import Weapon, Character

class WeaponForm(forms.ModelForm):
    name = forms.CharField(label='무기 이름')
    power = forms.IntegerField(label='무기 공격력')

    class Meta:
        model = Weapon
        fields = '__all__'

class CharacterForm(forms.ModelForm):
    nickname = forms.CharField(label="닉네임을 입력해주세요")

    class Meta:
        model = Character
        fields = ['nickname',]
