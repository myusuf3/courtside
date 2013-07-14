from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from forms.forms import GameForm
from game.models import Player, Sport, Game


def about(request):
    return render(request, 'about.html')


def home(request):
    """ This method deals with the profile for the user who just signed in.
        It will display upcoming games that the user is interested in and games they said they would be part of.

        I will also display some user info.
    """
    if not request.user.is_authenticated():
        soccer = Game.objects.filter(sport=Sport.objects.get(sport="soccer"), active="true")
        volleyball = Game.objects.filter(sport=Sport.objects.get(sport="volleyball"), active="true")
        baseball = Game.objects.filter(sport=Sport.objects.get(sport="baseball"), active="true")
        hockey = Game.objects.filter(sport=Sport.objects.get(sport="hockey"), active="true")
        basketball = Game.objects.filter(sport=Sport.objects.get(sport="basketball"), active="true")
        return render(request, 'index.html', {'soccer': soccer, 'hockey': hockey, 'basketball': basketball, 'baseball': baseball, 'volleyball': volleyball})

    if request.user.is_staff:
        return HttpResponseRedirect('/admin/')

    player = Player.objects.get(user=request.user)
    sports = player.sports.all()
    joined_games = player.game_set.all()
    my_games = Game.objects.filter(owner=request.user)
    profile_pic_url = player.image_url
    return render(request, 'profile.html', {'player': player, 'profile_pic_url': profile_pic_url, 'sports': sports, 'games': my_games | joined_games})


@login_required(login_url='/login/')
def create(request):
    """ User will create games.

        Keyword arguments:
        request -
    """
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            sport = Sport.objects.get(sport=form.cleaned_data['sport'])
            #player = Player.objects.get(user=request.user) # unused var

            game = Game()
            game.sport = sport
            game.owner = request.user
            game.start_date_and_time = datetime.combine(form.cleaned_data['start_date'], form.cleaned_data['start_time'])
            game.address = form.cleaned_data['address']
            game.minimum_players = form.cleaned_data['minimum_players']
            game.restrictions = form.cleaned_data['restrictions']
            game.active = True

            if request.POST['lng'] and request.POST['lat']:
                game.longitude = request.POST['lng']
                game.latitude = request.POST['lat']
                game.save()

                return HttpResponseRedirect('/game/%s/' % game.id)

    else:
        form = GameForm()
    return render(request, 'create.html', {'form': form})


def game(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    owner = Player.objects.get(user=game.owner)
    players = game.players.all()
    # +1 For the owner
    number_of_players = len(players) + 1
    joined = False

    if request.user.is_authenticated():
        current_player = Player.objects.get(user=request.user)
        current_games = current_player.game_set.all()
        if game in current_games:
            joined = True

    else:
        current_player = None

    game.sport.name = game.sport.sport.lower()
    return render(request, 'game.html', {'game': game, 'players': players, 'current_player': current_player, 'joined': joined, 'number_of_players': number_of_players, 'owner': owner})


@login_required(login_url='/login/')
def join(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    player = Player.objects.get(user=request.user)
    game.players.add(player)
    return HttpResponseRedirect('/game/%s/' % game_id)


@login_required(login_url='/login/')
def leave(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    player = Player.objects.get(user=request.user)
    game.players.remove(player)
    return HttpResponseRedirect('/game/%s/' % game_id)


@login_required(login_url='/login/')
def delete(request, game_id):
    game = get_object_or_404(Game, pk=game_id)

    if request.user != game.owner:
        return HttpResponseRedirect('/game/%s/' % game_id)

    game.players.clear()
    game.delete()

    return HttpResponseRedirect('/')


@login_required(login_url='/login/')
def search(request):
    player = Player.objects.get(user=request.user)
    sports = {}
    for sport in player.sports.all():
        sports[sport.sport] = True

    games = {}
    games['soccer'] = Game.objects.filter(sport=Sport.objects.get(sport="soccer"), active="true")
    games['volleyball'] = Game.objects.filter(sport=Sport.objects.get(sport="volleyball"), active="true")
    games['baseball'] = Game.objects.filter(sport=Sport.objects.get(sport="baseball"), active="true")
    games['hockey'] = Game.objects.filter(sport=Sport.objects.get(sport="hockey"), active="true")
    games['basketball'] = Game.objects.filter(sport=Sport.objects.get(sport="basketball"), active="true")
    return render(request, 'search.html', {'games': games, 'sports': sports})
