from django.conf.urls.defaults import patterns, include, url

from chat.views import (
        room,
        room_list,
        socketio
)

urlpatterns = patterns('',

    # A list of chatrooms
    url(
        regex=r'^$',
        view=room_list,
        name='room_list'
    ),

    # A specific chatroom
    url(
        regex=r'^room/(?P<room_name>.*)$',
        view=room,
        name='room'
    ),

    # Socket IO hook
    url(
        regex=r'^socket\.io',
        view=socketio,
        name='socketio'
    ),
)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
