from flask import Flask


from briscola.endpoint.lobby_endpoint import lobby_endpoint

# initialize Flask
app = Flask(__name__)


app.register_blueprint(lobby_endpoint, url_prefix='/lobbies')


# @app.route("/lobbies", methods=["GET"])
# def foo():
#     pass

# @app.route("/", methods=["GET", "POST"])
# def index():
#     """Serve the index HTML"""
#     return render_template("index.html")


if __name__ == "__main__":
    Flask.run(app, host="0.0.0.0", debug=True)
