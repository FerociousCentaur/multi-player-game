from django.urls import path

from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', home, name="home"),
    path('play/<room_code>', play, name="play"),
    path('close/', close_room, name="close_room"),
    path('get_players', get_players, name="get_players"),
    path('shuffle', shuffle, name="shuffle"),
    path('play_chance', play_chance, name="play_chance"),
    path('get_cards', get_cards, name="get_cards"),
    path('first_player', first_player, name="first_player"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
