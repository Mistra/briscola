from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, emit, send
import game
import random
import string
import json

# initialize Flask
app = Flask(__name__)
socketio = SocketIO(app)

# dict to track active rooms  
ROOMS = {}  # room_id: {'room_size': 2/3/4, 'players': ['sessions_id', 'sessions_id', ...]}

# dict to track active users
USERS = {}  # session_id: {'user_name': 'name', 'room': room_id}

@app.route('/', methods=['GET', 'POST'])
def index():
    """Serve the index HTML"""
    return render_template('index.html')


@socketio.on('create')
def on_create(data):
    """Create a game lobby"""
    user = data['username']
    session_id = request.sid
    if data['players_number'] == 'join':
        return
    players_number = int(data['players_number'])
    if session_id in USERS and USERS[session_id]['room'] != '':
        print (session_id + " already in a room")
        return
    if not session_id in USERS:
        USERS[session_id] = {'username': '', 'room': ''}
    room_id = generate_room_id()
    join_room(room_id)
    message = {'username': user, "session": session_id, 'room': room_id}
    message = json.dumps(message)
    emit('joined_user', message)
    ROOMS[room_id] = {}
    ROOMS[room_id]["room_size"] = players_number
    ROOMS[room_id]["players"] = [session_id]
    USERS[session_id]['username'] = user
    USERS[session_id]['room'] = room_id
    print(ROOMS)
    print(USERS)
    update_client_users_list(room_id)
    send_print_users()


@socketio.on('join')
def on_join(data):
    """Join a game lobby"""
    user = data['username']
    session_id = request.sid
    if not session_id in USERS:
        USERS[session_id] = {'user_name': '', 'room': ''}
    room_id = data['room']
    if room_id in ROOMS:
        room_size = ROOMS[room_id]["room_size"]
        players_number = len(ROOMS[room_id]["players"])
        if players_number < room_size:
            if not session_id in ROOMS[room_id]["players"]:
                join_room(room_id)
                message = {
                    "username": user,
                    "session": session_id,
                    "room": room_id
                }
                message = json.dumps(message)
                emit("joined_user", message, room=room_id)
                ROOMS[room_id]["players"].append(session_id)
                USERS[session_id]['username'] = user
                USERS[session_id]['room'] = room_id
                update_client_users_list(room_id)
                send_print_users()
                print(ROOMS)
                print(USERS)
        else:
            message = {"code_error": "0", "error_msg": "The room is full you can't join it"}
            message = json.dumps(message)
            emit("error", message)
    else:
        message = {'code_error': "1", "error_msg": "Unable to join room. Room does not exist."}
        message = json.dumps(message)
        emit('error', message)

@socketio.on('disconnect')
def on_disconnect():
    """Join a game lobby"""
    # TODO: Verify that this solution does not have concurrency problems
    session_id = request.sid
    if USERS[session_id]['room'] in ROOMS:
        if len(ROOMS[USERS[session_id]['room']]["players"]) < 2:
            del ROOMS[USERS[session_id]['room']]
        else:
            ROOMS[USERS[session_id]['room']]["players"].remove(session_id)
    del USERS[session_id]
    print("a user disconnected")


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
    for session_id in ROOMS[room]["players"]:
        json_object.append({"username": USERS[session_id]['username'], "session": session_id})
    json_object = json.dumps(json_object)
    emit('active_users', json_object, room=room)

def clean_empty_rooms(session_id):
    """This function checks for empty ROOMS and delete them from the dictionary"""
    
    pass

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=False)