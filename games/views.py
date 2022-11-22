from django.shortcuts import render, redirect, get_object_or_404
from random import *
from .models import Weapon, Character, Enemy
from .forms import WeaponForm, CharacterForm
# [미션] 자유롭게 코드 작성
# [미션] 코드에 필요한 모듈 불러오기


# Create your views here.
win = 0
draw = 0
lose = 0

# 무기 생성 함수
def weapon_generate():
    # 추가하고 싶은 무기가 있다면 추가 가능
    # weapons 딕셔너리의 key 값은 무기 이름, value 값은 무기 공격력
    weapons = {
        '주먹도끼': 2,
        '가벼운 물총': 3,
        '낡은 검': 5,
        '수상한 막대기': 7,
        '수학의 정석': 9,
    }
    # weapon_name에는 weapons 딕셔너리의 key 값이 저장됨
    for weapon_name in weapons:
        # weapon_name에 해당하는 무기가 없는 경우 새로운 Weapon 객체 생성
        if Weapon.objects.filter(name=weapon_name).count() == 0:
            Weapon.objects.create(
                name = weapon_name,
                power = weapons[weapon_name],
            )

# 적 생성 함수
def enemy_generate():
    # 추가하고 싶은 적이 있다면 추가 가능
    # enemies 딕셔너리의 key 값은 적 이름, value 값은 적 hp
    enemies = {
        '흩날리는 종이': 10,
        '뒤집어진 냄비': 25,
        '수수한 독버섯': 50,
        '수학 공식': 85,
        '아기 용': 100,
    }
    # enemy_name에는 enemies 딕셔너리의 key 값이 저장됨
    for enemy_name in enemies:
        # enemy_name에 해당하는 적이 없는 경우 새로운 Enemy 객체 생성
        if Enemy.objects.filter(name=enemy_name).count() == 0:
            Enemy.objects.create(
                name = enemy_name,
                hp = enemies[enemy_name],
            )

def game_list(request):
    # 무기를 생성할 필요가 없는 경우 weapon_generate() 함수를 주석으로 달아놓기
    weapon_generate()
    # 적을 생성할 필요가 없는 경우 enemy_generate() 함수를 주석으로 달아놓기
    enemy_generate()
    return render(request, 'games/game_list.html')

def rsp_select(request):
    global win, draw, lose
    context = {
        'win': win,
        'draw': draw,
        'lose': lose,
    }
    return render(request, 'games/rsp_select.html', context)

def rsp_result(request, pick):
    global win, draw, lose
    rsp = ['가위', '바위', '보']
    com = choice(rsp)

    if pick == com:
        result = '무승부'
        draw += 1
    elif (pick == '가위' and com == '보') or (pick == '바위' and com == '가위') or (pick == '보' and com == '바위'):
        result = '승리'
        win += 1
    else :
        result = '패배'
        lose += 1

    context = {
        'pick': pick,
        'com': com,
        'result': result,
        'win': win,
        'draw': draw,
        'lose': lose,
    }
    return render(request, 'games/rsp_result.html', context)

def rsp_reset(request):
    global win, draw, lose
    win, draw, lose = 0, 0, 0
    return redirect('games:rsp_select')

def weapon_create(request):
    if request.method == 'POST':
        weapon_form = WeaponForm(request.POST)
        
        if weapon_form.is_valid():
            weapon_form.save()
            return redirect('games:weapon_list')
    else:
        weapon_form = WeaponForm()
    
    context = {
        'weapon_form': weapon_form,
    }
    return render(request, 'games/weapon_form.html', context)

def weapon_list(request):
    weapons = Weapon.objects.all()
    context = {
        'weapons': weapons,
    }
    return render(request, 'games/weapon_list.html', context)

def adventure_home(request):
    # 로그인 한 경우
    if request.user.is_authenticated:
        # 생성한 캐릭터가 없을 경우
        # filter를 이용하여 로그인 한 유저와 연결되어 있는 캐릭터 객체가 있는지 찾음
        if Character.objects.filter(user=request.user).count() == 0:
            if request.method == 'POST':
                character_form = CharacterForm(request.POST)
                character_form = character_form.save(commit=False)
                character_form.user = request.user
                character_form.save()
                return redirect('games:adventure_home')
            else:
                character_form = CharacterForm()
            context = {
                'character_form': character_form,
            }
            return render(request, 'games/character_form.html', context)
        # 생성한 캐릭터가 있는 경우
        else:
            character = get_object_or_404(Character, user=request.user)
            # 무기를 얻지 못한 경우
            if character.weapon == None:
                # 무기 랜덤 선택
                # order_by('?')를 이용하여 랜덤하게 정렬 후 첫번째 항목을 가져옴
                random_weapon = Weapon.objects.order_by('?')[0]
                context = {
                    'random_weapon': random_weapon,
                }
                return render(request, 'games/adventure_new.html', context)
            # 무기를 얻은 경우
            else:
                context = {
                    'character': character,
                }
                return render(request, 'games/adventure_home.html', context)
    # 로그인 하지 않은 경우
    else:
        return redirect('accounts:login')

def weapon_get(request):
    if request.method == 'POST':
        character = get_object_or_404(Character, user=request.user)

        weapon_id = request.POST.get('random-weapon')
        selected_weapon = get_object_or_404(Weapon, id=weapon_id)
        
        character.weapon = selected_weapon
        character.save()
    return redirect('games:adventure_home')

# 모험 떠나기
def adventure_attack(request):
    # 랜덤 적 생성
    random_enemy = Enemy.objects.order_by('?')[0]
    
    context = {
        'random_enemy': random_enemy,
    }
    return render(request, 'games/adventure_attack.html', context)

def adventure_attack_result(request):
    # 로그인 한 유저의 캐릭터
    character = get_object_or_404(Character, user=request.user)

    # 캐릭터와 마주친 랜덤 적
    enemy_id = request.POST.get('random-enemy')
    enemy = get_object_or_404(Enemy, id=enemy_id)
    
    # [미션] 자유롭게 코드 작성
    # [미션] 필요 시 context 작성 후 html 페이지에 전달

    return render(request, 'games/adventure_attack_result.html')

# 무기 공방
def weapon_workroom(request):
    character = get_object_or_404(Character, user=request.user)

    context = {
        'character': character,
        'weapon_name': character.weapon.name,
        'weapon_power': character.weapon.power,
    }
    return render(request, 'games/weapon_workroom.html', context)

# [미션] 자유롭게 코드 작성
# [미션] 무기 뽑기, 교체 등의 기능을 가진 함수 구현

