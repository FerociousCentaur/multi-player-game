from django.contrib import messages
from django.core import serializers
# Create your views here.
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from .models import *


def home(request):
    if request.method == "POST":
        username = request.POST.get('username')
        option = request.POST.get('option')
        room_code = request.POST.get('room_code')
        print(room_code)
        if option == '1':
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
            user = Profile(name=username)
            user.save()
            game.players.add(user)
            game.save()
            return redirect('/play/' + room_code + '?username=' + username)
        else:
            user = Profile(name=username)
            user.save()
            game = Game(game_creator=username, room_code=room_code)
            game.save()
            game.players.add(user)
            game.save()
            return redirect('/play/' + room_code + '?username=' + username)

    return render(request, 'home.html')


@csrf_exempt
def close_room(request):
    room_code = request.POST.get("room_code")

    game = Game.objects.get(room_code=room_code)
    if game.is_in_progress:
        data = {"message": "Already cloased"}
        return JsonResponse(data)
    game.is_in_progress = True
    game.save()
    # return redirect('/play/' + room_code + '?username='+username)
    data = {"message": "closed"}
    return JsonResponse(data)


def play(request, room_code):
    username = request.GET.get('username')
    context = {'room_code': room_code, 'username': username}
    return render(request, 'play.html', context)


@csrf_exempt
def get_players(request):
    data = request.POST
    room = data.get('room_code', None)
    game = Game.objects.get(room_code=room)
    closed = False
    if game.is_in_progress:
        closed = True
    players = game.players.all()
    data = serializers.serialize('json', players)
    return JsonResponse({"data": data, "closed": closed})

