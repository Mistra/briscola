from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, emit, send
from briscola import game

# initialize Flask
app = Flask(__name__)
socketio = SocketIO(app)
ROOMS = {} # dict to track active rooms

@app.route('/', methods=['GET', 'POST'])
def index():
    """Serve the index HTML"""
    return render_template('index.html')

@socketio.on('create')
def on_create(data):
    """Create a game lobby"""
    gm = game.Game(
        username = data['username']
    )
    
    gm.deck.shuffle()

    print(gm.deck.cards)
    print(gm.players)
    room = gm.game_id
    ROOMS[room] = gm
    join_room(room)
    emit('join_room', {'room': room})

@socketio.on('join')
def on_join(data):
    """Join a game lobby"""
    # username = data['username']
    room = data['room']
    if room in ROOMS:
        # add player and rebroadcast game object
        # rooms[room].add_player(username)
        join_room(room)
        send(ROOMS[room].to_json(), room=room)
    else:
        emit('error', {'error': 'Unable to join room. Room does not exist.'})

if __name__ == '__main__':
    socketio.run(app, debug=False)