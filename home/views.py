import uuid
import random
from django.contrib import messages
from django.core import serializers
# Create your views here.
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from .models import *

cards = ['Club_1', 'Club_10', 'Club_11', 'Club_12', 'Club_13', 'Club_2', 'Club_3', 'Club_4', 'Club_5', 'Club_6',
         'Club_7', 'Club_8', 'Club_9', 'Diamond_1', 'Diamond_10', 'Diamond_11', 'Diamond_12', 'Diamond_13', 'Diamond_2',
         'Diamond_3', 'D\
iamond_4', 'Diamond_5', 'Diamond_6', 'Diamond_7', 'Diamond_8', 'Diamond_9', 'Heart_1', 'Heart_10', 'Heart_11',
         'Heart_12', 'Heart_13', 'Heart_2', 'Heart_3', 'Heart_4', 'Heart_5', 'Heart_6', 'Heart_7', 'Heart_8', 'Heart_9',
         'Spade_1', 'Spade_10', 'Spade_11', 'Spade_12', 'Spade_13', 'Spade_2', 'Spade_3', 'Spade_4', 'Spade_5',
         'Spade_6', 'Spade_7', 'Spade_8', 'Spade_9']

@csrf_exempt
def home(request):
    if request.method == "POST":
        username = request.POST.get('username')
        option = request.POST.get('option')
        # room_code = request.POST.get('room_code')
        # print(room_code)
        if option == '1':
            room_code = request.POST.get('room_code')
            game = Game.objects.filter(room_code=room_code).first()

            if game is None:
                messages.success(request, "Room code not found")
                return redirect('/')

            if game.is_over:
                messages.success(request, "Game is over")
                return redirect('/')

            if game.is_in_progress:
                messages.success(request, "Sorry the game has already started")
                return redirect('/')
            user = Profile.objects.create(name=username, uid=str(uuid.uuid4())[:7])
            uid = user.uid
            game.players.add(user)
            game.save()
            return redirect('/play/' + room_code + '?uid=' + uid)
        else:
            user = Profile.objects.create(name=username, uid=str(uuid.uuid4())[:7])
            uid = user.uid
            game = Game.objects.create(game_creator=uid, room_code=str(uuid.uuid4())[:7], folded_cards=cards)
            game.players.add(user)
            game.save()
            return redirect('/play/' + game.room_code + '?uid=' + uid)

    return render(request, 'home.html')


@csrf_exempt
def close_room(request):
    room_code = request.POST.get("room_code")
    uid = request.POST.get("uid")
    game = Game.objects.get(room_code=room_code)
    if game.is_in_progress:
        data = {"message": "Already cloased"}
        return JsonResponse(data)
    elif uid == game.game_creator:
        game.is_in_progress = True
        game.save()
        # return redirect('/play/' + room_code + '?username='+username)
        data = {"message": "closed"}
    else:
        data = {"message": "Unothorised"}
    return JsonResponse(data)


@csrf_exempt
def first_player(request):
    room_code = request.POST.get("room_code")
    game = Game.objects.get(room_code=room_code)
    players = game.players.all()
    li = []
    for player in players:
        li.append(player.uid)
    fp = random.choice(li)
    return JsonResponse({"uid": fp})

def shuffler(game_cards):
    random.shuffle(game_cards)


@csrf_exempt
def shuffle(request):
    required = 5
    room_code = request.POST.get("room_code")
    uid = request.POST.get("uid")
    game = Game.objects.get(room_code=room_code)
    if not game.is_in_progress:
        return JsonResponse({"status": "First close the room"})
    game_cards = cards#eval(game.folded_cards)
    shuffler(game_cards)
    players = game.players.all()
    itera = 0
    n = len(players)
    for player in players:
        pl_card = []
        start = itera
        while len(pl_card) < required:
            pl_card.append(game_cards[start + n * len(pl_card)])
        player.cards = pl_card
        player.save()
        itera += 1
    game.unfolded_cards = str([game_cards[required*n+1]])
    game.folded_cards = game_cards[required*n+2:]
    game.save()
    return JsonResponse({"status": "Done"})

@csrf_exempt
def get_cards(request):
    data = request.POST
    uid = data.get('uid', None)
    room_code = data.get('room_code', None)
    player = Profile.objects.get(uid=uid)
    game = Game.objects.get(room_code=room_code)
    return JsonResponse({"player_cards": eval(player.cards), "unfolded_cards": eval(game.unfolded_cards)})


@csrf_exempt
def play_chance(request):
    data = request.POST
    uid = data.get('uid', None)
    room_code = data.get('room_code', None)
    player = Profile.objects.get(uid=uid)
    game = Game.objects.get(room_code=room_code)
    # var
    # arr = [1, 2, 3, 4];
    #
    # $.ajax({
    #     url: '...',
    #     type: 'POST',
    #     data: {'arr': arr},
    # });
    played_cards = data.getlist('played[]', None)
    res = list(filter(lambda i: i not in played_cards, eval(player.cards)))
    folded = data.get('folded', None)
    if folded=='true':
        f_cards = eval(game.folded_cards)
        picked = f_cards.pop()
        game.folded_cards = f_cards
        game.unfolded_cards = played_cards
        game.save()
        res.append(picked)
        player.cards = res
        player.save()
    else:
        picked = data.get('picked', None)
        res.append(picked)
        player.cards = res
        player.save()
        game.unfolded_cards = played_cards
        game.save()
    return JsonResponse({"picked": picked})



@csrf_exempt
def play(request, room_code):
    uid = request.GET.get('uid')
    creator = False
    game = Game.objects.get(room_code=room_code)
    if game.game_creator == uid:
        creator = True
    context = {'room_code': room_code, 'uid': uid, 'creator': creator}
    return render(request, 'play.html', context)


@csrf_exempt
def get_players(request):
    data = request.POST
    room = data.get('room_code', None)
    game = Game.objects.filter(room_code=room).first()
    if game:
        closed = False
        if game.is_in_progress:
            closed = True
        players = game.players.all()
        data = serializers.serialize('json', players)
        return JsonResponse({"data": data, "closed": closed})
    else:
        return JsonResponse({"closed": "DNE"})
