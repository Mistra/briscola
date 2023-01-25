# Briscola Web App
[Briscola] is an Italian card game.

- Backend written in [flask]
- Frontend - To be decided

### Installation

Briscola requires [Python3] to run.

Create a virtualenv where to install dependencies
```sh
$ python3 -m venv venv
```
Install the dependencies and start the server.

```sh
$ pip install -r requirements.txt
$ flask run
```

### Todos
- Create DTOs (actually 2 player and game)
- See if GameRepository can be used as a master repo when game needs to be created (refactoring needed?)

License
----

MIT

[Briscola]: <https://en.wikipedia.org/wiki/Briscola>
[Flask]: <https://flask.palletsprojects.com/en/1.1.x/>
[Python3]: <https://www.python.org/>