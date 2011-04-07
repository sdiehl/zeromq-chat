import time
from simplejson import dumps
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext

# ZeroMQ Connection
from gevent import spawn
from gevent_zeromq import zmq

context = zmq.Context()
publisher = context.socket(zmq.PUB)
publisher.bind("tcp://127.0.0.1:5000")

ACTIVE_ROOMS = set([])

# Message Coroutines

def send_message(socket, room, text):
    socket.send_unicode("%s:%s" % (room, text))

def message_listener(socketio, room):
    context = zmq.Context()
    subscriber = context.socket(zmq.SUB)
    subscriber.connect("tcp://127.0.0.1:5000")

    # setsockopt doesn't like unicode
    subscriber.setsockopt(zmq.SUBSCRIBE, str(room))

    socketio.send({'message': 'connected: ' + room})

    while True:
        msg = subscriber.recv()
        if msg:
            socketio.send({'message': msg.split(":")[1]})

# Room Coroutines

def new_room(socket, room_name):
    socket.send("room:%s" % str(room_name))

def room_listener(socketio):
    context = zmq.Context()
    subscriber = context.socket(zmq.SUB)
    subscriber.connect("tcp://127.0.0.1:5000")
    subscriber.setsockopt(zmq.SUBSCRIBE, 'room')

    while True:
        msg = subscriber.recv()
        if msg:
            socketio.send({'room_name': msg.split(":")[1]})

        time.sleep(5)

def room(request, room_name=None, template_name='room.html'):
    context = {
        'room_name': room_name,
        'initial_rooms': dumps(list(ACTIVE_ROOMS)),
    }

    if room_name not in ACTIVE_ROOMS:
        spawn(new_room, publisher, room_name)
        ACTIVE_ROOMS.add(room_name)

    return render_to_response(template_name, context,
            context_instance=RequestContext(request))

def room_list(request, template_name='room_list.html'):
    context = {
        'initial_rooms': dumps(list(ACTIVE_ROOMS)),
    }

    return render_to_response(template_name, context,
            context_instance=RequestContext(request))

# SocketIO Handler

def socketio(request):
    socketio = request.environ['socketio']

    while True:
        message = socketio.recv()

        if len(message) == 1:
            action, arg = message[0].split(':')

            if action == 'subscribe':

                if arg == 'rooms':
                    spawn(room_listener, socketio)
                else:
                    spawn(message_listener, socketio, arg)

            elif action == 'message':
                room, text = arg.split(',')

                #timestamp = time.strftime("(%H.%M.%S)", time.localtime())
                ip_addr = request.META['REMOTE_ADDR']
                message = "(%s)  %s" % (ip_addr, text)
                spawn(send_message, publisher, room, message).join()

    return HttpResponse()


