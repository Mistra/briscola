
import logging
import os

from flask import Flask

from src.endpoint.lobby_endpoint import lobby_endpoint
from src.endpoint.player_endpoint import player_endpoint

# initialize Flask
app = Flask(__name__)

app.config.from_mapping(
    # a default secret that should be overridden by instance config
    SECRET_KEY=os.environ.get('SECRET_KEY') or 'you-will-never-guess',
    # store the database in the instance folder
    DATABASE=os.path.join("database/development.db"),
)

app.register_blueprint(lobby_endpoint, url_prefix='/lobbies')
app.register_blueprint(player_endpoint, url_prefix='/players')

# The following line sets the root logger level as well.
# It's equivalent to both previous statements combined:
logging.basicConfig(level=logging.NOTSET)

if __name__ == "__main__":
    Flask.run(app, host="0.0.0.0", debug=True)