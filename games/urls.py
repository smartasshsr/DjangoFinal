from django.urls import path
from . import views

app_name = 'games'

urlpatterns = [
    path('', views.game_list, name='game_list'),
    path('rsp/', views.rsp_select, name='rsp_select'),
    path('rsp/<str:pick>', views.rsp_result, name='rsp_result'),
    path('rsp/reset/', views.rsp_reset, name='rsp_reset'),
    path('weapon/create/', views.weapon_create, name='weapon_create'),
    path('weapon/list/', views.weapon_list, name='weapon_list'),
    path('adventure/home/', views.adventure_home, name='adventure_home'),
    path('weapon/get/', views.weapon_get, name='weapon_get'),
    path('adventure/attack/', views.adventure_attack, name='adventure_attack'),
    path('adventure/attack/result/', views.adventure_attack_result, name='adventure_attack_result'),
    path('weapon/workroom/', views.weapon_workroom, name='weapon_workroom'),
    path('weapon/pick/', views.weapon_pick, name='weapon_pick'),
    path('weapon/change/', views.weapon_change, name='weapon_change'),
]
