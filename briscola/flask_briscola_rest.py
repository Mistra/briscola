from flask import Flask, render_template, request
import random
import string
import json

# initialize Flask
app = Flask(__name__)
# dict to track active rooms
ROOMS = (
    {}
)  # room_id: {'room_size': 2/3/4, 'players': ['sessions_id', 'sessions_id', ...]}

# dict to track active users
USERS = {}  # session_id: {'user_name': 'name', 'room': room_id}


@app.route("/", methods=["GET", "POST"])
def index():
    """Serve the index HTML"""
    return render_template("index.html")


def generate_room_id():
    """Generate a random room ID"""
    id_length = 5
    return "".join(
        random.SystemRandom().choice(string.ascii_uppercase) for _ in range(id_length)
    )


if __name__ == "__main__":
    Flask.run(app, host="0.0.0.0", debug=False)
