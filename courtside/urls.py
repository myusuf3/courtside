from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.contrib import admin
from tastypie.api import Api

from game.api import (GameResource, UserResource, PlayerResource,
SportResource)

v1_api = Api(api_name='v1')
v1_api.register(GameResource())
v1_api.register(UserResource())
v1_api.register(PlayerResource())
v1_api.register(SportResource())


admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'courtside.views.home', name='home'),
    url(r'^about/', 'game.views.about', name='about'),

    url(r'^$', 'game.views.home', name='home'),
    
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    #regular signup
    url(r'^login/signup/', 'register.views.new_register', name='regular_signup'),

    #login complete
    url(r'^login/complete/', 'register.views.complete_sign_up'),

    #twitter stuff
	url(r'^login/twitter/', 'register.views.begin_twitter_oauth', name='twitter_oauth'),
    url(r'^twitter/callback/', 'register.views.twitter_callback'),
    
    #edit profile
    url(r'^profile/edit/', 'register.views.profile_edit'),

    #facebook stuff
    url(r'^login/facebook/', 'register.views.begin_facebook_oauth', name='facebook_oauth'),
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

    #api endpoints
     (r'^api/', include(v1_api.urls)),

)


