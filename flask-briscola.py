from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, emit, send
from briscola import game
import random
import string
import json

# initialize Flask
app = Flask(__name__)
socketio = SocketIO(app)
ROOMS = {}  # dict to track active rooms


@app.route('/', methods=['GET', 'POST'])
def index():
    """Serve the index HTML"""
    return render_template('index.html')


@socketio.on('create')
def on_create(data):
    """Create a game lobby"""
    user = data['username']
    session_id = request.sid
    room_id = generate_room_id()
    join_room(room_id)
    message = {'username': user, "session": session_id, 'room': room_id}
    message = json.dumps(message)
    emit('joined_user', message)
    ROOMS[room_id] = [(user, session_id)]
    update_client_users_list(room_id)


@socketio.on('join')
def on_join(data):
    """Join a game lobby"""
    user = data['username']
    session_id = request.sid
    room_id = data['room']
    if room_id in ROOMS:
        if not any(user in i for i in ROOMS[room_id]):
            join_room(room_id)
            message = {
                'username': user,
                "session": session_id,
                'room': room_id
            }
            message = json.dumps(message)
            emit("joined_user", message, room=room_id)
            ROOMS[room_id].append((user, session_id))
            update_client_users_list(room_id)
            send_print_users()
    else:
        emit('error', {'error': 'Unable to join room. Room does not exist.'})


def generate_room_id():
    """Generate a random room ID"""
    id_length = 5
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase)
                   for _ in range(id_length))


def send_print_users():
    """Send an event to users to say hello to a new user"""
    emit('print_users', broadcast=True)


def update_client_users_list(room):
    """Send an event to users to update the list of connected users in a room"""
    json_object = []
    for user, session_id in ROOMS[room]:
        json_object.append({"username": user, "session": session_id})
    json_object = json.dumps(json_object)
    emit('active_users', json_object, room=room)


if __name__ == '__main__':
    socketio.run(app, debug=False)
