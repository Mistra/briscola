
import logging
import os

from flask import Flask

from src.endpoint.player_endpoint import player_endpoint

# initialize Flask
app = Flask(__name__)

app.config.from_mapping(
    # a default secret that should be overridden by instance config
    SECRET_KEY=os.environ.get('SECRET_KEY') or 'you-will-never-guess',
    # store the database in the instance folder
    DATABASE=os.path.join("database/development.db"),
)

app.register_blueprint(player_endpoint, url_prefix='/players')

# The following line sets the root logger level as well.
# It's equivalent to both previous statements combined:
logging.basicConfig(level=logging.DEBUG)


def pirate_game():
    logging.debug("Starting pirate game")


if __name__ == "__main__":

    pirate_game()
    app.logger.info('%s logged in successfully', "user.username")
    Flask.run(app, host="0.0.0.0", debug=True)
