from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
admin.autodiscover()

from rest_framework.urlpatterns import format_suffix_patterns
from game import api



urlpatterns = patterns(
    '',
    url(r'^about/', 'game.views.about', name='about'),
    url(r'^$', 'game.views.home', name='home'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    #regular signup
    url(r'^login/signup/', 'register.views.new_register',
        name='regular_signup'),

    #login complete
    url(r'^login/complete/', 'register.views.complete_sign_up'),

    #twitter stuff
    url(r'^login/twitter/', 'register.views.begin_twitter_oauth',
        name='twitter_oauth'),
    url(r'^twitter/callback/', 'register.views.twitter_callback'),

    #edit profile
    url(r'^profile/edit/', 'register.views.profile_edit'),

    #facebook stuff
    url(r'^login/facebook/', 'register.views.begin_facebook_oauth',
        name='facebook_oauth'),
    url(r'^facebook/callback/', 'register.views.facebook_callback'),

    url(r'^logout/', 'register.views.logout_bro', name='logout'),
    url(r'^login/', 'register.views.login_bro', name='logout'),


    url(r'^create/', 'game.views.create', name='create'),
    url(r'^search/', 'game.views.search', name='search'),
    url(r'^game/(?P<id>\d+)/$', 'game.views.game', name='game'),
    url(r'^join/game/(?P<id>\d+)/$', 'game.views.join', name='join'),
    url(r'^leave/game/(?P<id>\d+)/$', 'game.views.leave', name='leave'),
    url(r'^delete/game/(?P<id>\d+)/$', 'game.views.delete', name='delete'),

    # comments application
    (r'^comments/', include('django.contrib.comments.urls')),

    # API
    url(r'^api/games/$', api.GameList.as_view()),
    url(r'^api/games/(?P<pk>[0-9]+)/$', api.GameDetail.as_view()),
)

urlpatterns = format_suffix_patterns(urlpatterns)
