from django.contrib import messages
from django.core import serializers
# Create your views here.
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from .models import *
import uuid

cards = ['Club_1', 'Club_10', 'Club_11', 'Club_12', 'Club_13', 'Club_2', 'Club_3', 'Club_4', 'Club_5', 'Club_6', 'Club_7', 'Club_8', 'Club_9', 'Diamond_1', 'Diamond_10', 'Diamond_11', 'Diamond_12', 'Diamond_13', 'Diamond_2', 'Diamond_3', 'D\
iamond_4', 'Diamond_5', 'Diamond_6', 'Diamond_7', 'Diamond_8', 'Diamond_9', 'Heart_1', 'Heart_10', 'Heart_11', 'Heart_12', 'Heart_13', 'Heart_2', 'Heart_3', 'Heart_4', 'Heart_5', 'Heart_6', 'Heart_7', 'Heart_8', 'Heart_9', 'Spade_1', 'Spade_10', 'Spade_11', 'Spade_12', 'Spade_13', 'Spade_2', 'Spade_3', 'Spade_4', 'Spade_5', 'Spade_6', 'Spade_7', 'Spade_8', 'Spade_9']

def home(request):
    if request.method == "POST":
        username = request.POST.get('username')
        option = request.POST.get('option')
        #room_code = request.POST.get('room_code')
        #print(room_code)
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
    elif uid==game.game_creator:
        game.is_in_progress = True
        game.save()
        # return redirect('/play/' + room_code + '?username='+username)
        data = {"message": "closed"}
    else:
        data = {"message": "Unothorised"}
    return JsonResponse(data)


def shuffler(cards):
    pass

@csrf_exempt
def shuffle(request):
    room_code = request.POST.get("room_code")
    uid = request.POST.get("uid")
    game = Game.objects.get(room_code=room_code)
    cards =list(game.folded_cards)
    shuffler(cards)
    players = game.players.all()




def play(request, room_code):
    uid = request.GET.get('uid')
    creator = False
    game = Game.objects.get(room_code=room_code)
    if game.game_creator==uid:
        creator=True
    context = {'room_code': room_code, 'uid': uid, 'creator':creator}
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

