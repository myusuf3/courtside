import hashlib
import json
import urllib

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render
from forms.forms import PlayerForm, NewPlayerForm, ProfileForm, PasswordForm, LoginForm
from keys import keys
from models import Player
from twython import Twython as twitter



def get_gravatar(email, size=250):
    """ This method returns the url to the gravatar that
        corresponds to the email provided, at a default
        size of 100.

        Keyword arguments
        email - user's email address
        size - the size of the gravatar

    """
    h = hashlib.md5(email.lower()).hexdigest()
    image = "http://www.gravatar.com/avatar/%s?s=%s"  % (h, size)
    return image


def create_django_user(screen_name, twitter_oauth, email=None):
    """ This method creates a user object with the password
        set to the twitter oauth key. No email provided, twitter
        api limitation.

        Attention this only returns unsaved user.

        Keyword arguments
        screenname - twitter screenname
        email - email for this user; default None
        twitter_oauth - password for user using twitter key.

    """
    if email is None:
        user = User(username=screen_name)
        user.set_password(twitter_oauth)
    else:
        user = User.objects.create_user(screen_name, email, twitter_oauth)
    return user


def begin_twitter_oauth(request):
    """ This view will begin the user authentication process. It requires the
        consumer key and secret. link to the sign in with twitter.

        Keyword arguments:
        request -
    """
    twitter_conn = twitter(
        twitter_token = keys.CONSUMER_KEY,
        twitter_secret = keys.CONSUMER_SECRET
    )

    auth_prop = twitter_conn.get_authentication_tokens()
    request.session['request_token'] = auth_prop
    return HttpResponseRedirect(auth_prop['auth_url'])


def twitter_callback(request):
    """ This method deals with the callback needed by twitter, and creating the their user.

    """
    if 'denied' in request.GET:
        return HttpResponseRedirect('/')

    twitter_conn = twitter(
        twitter_token = keys.CONSUMER_KEY,
        twitter_secret = keys.CONSUMER_SECRET,
        oauth_token = request.session['request_token']['oauth_token'],
        oauth_token_secret = request.session['request_token']['oauth_token_secret']
    )

    auth_tokens = twitter_conn.get_authorized_tokens()

    try:
        user = User.objects.get(username = auth_tokens['screen_name'])
    except User.DoesNotExist:
        user = create_django_user(auth_tokens['screen_name'], auth_tokens['oauth_token_secret'])
        player = Player()
        player.user = user
        player.twitter_oauth_token = auth_tokens['oauth_token']
        player.twitter_oauth_secret = auth_tokens['oauth_token_secret']
        request.session['twitter'] = player
        form = PlayerForm(initial={'username': player.user.username})
        return render(request, 'register.html', {'form': form})
    player = Player.objects.get(user=user)
    user = authenticate(username=player.user.username, password=player.twitter_oauth_secret)
    login(request, user)
    return HttpResponseRedirect('/')


def complete_sign_up(request):
    """ This will use form object will be referenced here
        and used to fill in user data that is missing for twitter and facebook
        data.

        Keyword arguments:
        request -
    """
    if 'twitter' in request.session:
        if request.method == 'POST':
            form = PlayerForm(request.POST)
            if form.is_valid():
                player =  request.session['twitter']
                user =  player.user
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                #phone_number = form.cleaned_data['phone_number'] # unused
                sports = form.cleaned_data['sports']
                gender = form.cleaned_data['gender']
                player.gender = gender
                user.first_name = first_name
                user.last_name = last_name
                user.username = username
                user.email = email
                user.save()
                player.user = user
                player.image_url = get_gravatar(player.user.email)
                player.save()
                player.sports = sports
                user1 = authenticate(username=player.user.username, password=player.twitter_oauth_secret)
                login(request, user1)
                return HttpResponseRedirect('/')
        else:
            form = PlayerForm()
        return render(request, 'register.html', {'form': form})

    if 'facebook' in request.session:
        if request.method == 'POST':
            form = PlayerForm(request.POST)
            if form.is_valid():
                player =  request.session['facebook']
                user =  player.user
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                #phone_number = form.cleaned_data['phone_number'] # unused
                sports = form.cleaned_data['sports']
                gender = form.cleaned_data['gender']

                player.gender = gender
                user.first_name = first_name
                user.last_name = last_name
                user.username = username
                user.email = email
                user.save()
                player.user = user
                player.image_url = get_gravatar(player.user.email)
                player.sports = sports
                player.save()
                user = authenticate(username=player.user.username, password=player.facebook_oauth_token)
                login(request, user)
                return HttpResponseRedirect('/')
    else:
        form = PlayerForm()
    return render(request, 'register.html', {'form': form})


def new_register(request):
    """ This is for a new user who wishes to register independent of twitter and facebook;
        we use gravatar for these users.
    """
    if request.method == 'POST':
        form = NewPlayerForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            sports = form.cleaned_data['sports']
            gender = form.cleaned_data['gender']
            password1 = form.cleaned_data['password1']
            #password2 = form.cleaned_data['password2'] # unused

            user = User.objects.create_user(username=username, email=email, password=password1)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            player = Player()
            player.gender = gender
            player.user = user
            player.phone_number = phone_number
            player.image_url = get_gravatar(player.user.email)
            player.save()
            player.sports = sports
            user = authenticate(username=player.user, password=password1)
            login(request, user)
            # task here to email user
            SignUpTask.delay(user)
            return HttpResponseRedirect('/')
    else:
        if 'email' in request.GET:
            form = NewPlayerForm(initial={'email': request.GET['email']})
        else:
            form = NewPlayerForm()
    return render(request, 'new_register.html', {'form': form})

def begin_facebook_oauth(request):
    """
        This method creates a user object with the password
        set to the facebook access_token.

        Keyword arguments
        email - email for this user; default None
        facebook_oauth - password for user using access_token

    """
    args = dict(
        client_id = keys.FACEBOOK_APP_ID,
        redirect_uri = 'http://tini.ep.io/facebook/callback',
        scope = 'email'
    )

    url = 'http://www.facebook.com/dialog/oauth?' + urllib.urlencode(args)

    return HttpResponseRedirect(url)

def get_gender_initial(gender):
    """ This method given a facebook gender will convert it to form acceptable version.

        I am sure there is a better way to do this.
    """
    if str(gender) == 'male':
        return 'M'
    elif str(gender) == 'female':
        return 'F'
    else:
        return 'Q'


def facebook_callback(request):
    """ This method is responsible for the facebook callback and generating the facebook user.
    """

    if 'error' in request.GET:
        return HttpResponseRedirect('/')

    code = request.GET["code"]

    args = dict(
        client_id = keys.FACEBOOK_APP_ID,
        redirect_uri = 'http://tini.ep.io/facebook/callback',
        client_secret = keys.FACEBOOK_APP_SECRET,
        code = code
    )


    token_url = 'https://graph.facebook.com/oauth/access_token?' + urllib.urlencode(args)
    data = urllib.urlopen(token_url)
    response = data.read()
    data.close()

    # print 'Token URL:' + token_url
    # print 'Response:'
    # print response

    try:
        split = response.split('=')
        access_token = split[1].strip('&expires')
        expires = split[2]

        # print 'Access Token: ' + access_token
        # print 'Expires: ' + expires
    except:
        error = json.loads(response)
        return HttpResponseRedirect('/error')

    profile = json.load(urllib.urlopen('https://graph.facebook.com/me?' + urllib.urlencode(dict(access_token=access_token))))


    args = dict(
        access_token = access_token
    )

    graph_url = 'https://graph.facebook.com/me?' + urllib.urlencode(args)
    #print graph_url

    response = urllib.urlopen(graph_url)
    facebook_user = json.load(response)

    username = facebook_user.get('username', '')
    gender = facebook_user.get('gender', '')


    try:
        player = Player.objects.get(facebook_id=facebook_user.get('id', None))
    except ObjectDoesNotExist:
        user = User(username=username)
        user.set_password(access_token)
        user.first_name = facebook_user['first_name']
        user.last_name = facebook_user['last_name']
        user.email = facebook_user['email']

        player = Player()
        player.user = user
        player.gender = get_gender_initial(gender=gender)
        player.facebook_id = facebook_user['id']
        player.facebook_oauth_token = access_token
        request.session['facebook'] = player
        form = PlayerForm(initial={'username': player.user.username, 'first_name': user.first_name, 'last_name': user.last_name, 'email': player.user.email, 'gender': player.gender})
        return render(request, 'register.html', {'form': form})

    # player = Player.objects.get(user=user)
    # print player
    user = authenticate(username=player.user.username, password=player.facebook_oauth_token)
    login(request, user)
    return HttpResponseRedirect('/')


@login_required(login_url='/login/')
def profile_edit(request):
    user = request.user
    email = user.email
    player = Player.objects.get(user=user)
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            # print form.cleaned_data
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            player.gender = form.cleaned_data['gender']
            player.sports = form.cleaned_data['sports']
            player.phone_number = form.cleaned_data['phone_number']
            player.image_url = get_gravatar(user.email)
            user.save()
            player.save()
            return HttpResponseRedirect('/')
    else:
        player = Player.objects.get(user=user)
        # print player.sports.all()
        form = ProfileForm(initial={'username': player.user.username, 'first_name': user.first_name, 'last_name': user.last_name, 'email': player.user.email, 'gender': player.gender, 'sports': player.sports.all()})
    return render(request, 'profile_edit.html', {'form': form})


def login_bro(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # print form.cleaned_data
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            user = authenticate(username=user.username, password=password)
            # print user
            login(request, user)
            return HttpResponseRedirect('/')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form':form})


@login_required(login_url='/login/')
def password_edit(request):
    user = request.user
    email = user.email
    player = Player.objects.get(user=user)
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            # print form.cleaned_data
            password = form.cleaned_data['password']
            user.set_password()
            user.save()
            player.save()
            return HttpResponseRedirect('/')
    else:
        player = Player.objects.get(user=user)
    form = PasswordForm()


def logout_bro(request):
    """
    Standard logout view
    """
    logout(request)
    return HttpResponseRedirect('/')
