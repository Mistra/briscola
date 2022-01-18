# import json
# from briscola.flask_briscola_rest import app
# from flask import current_app
# import pytest


# @pytest.fixture
# def client():
#     with app.test_client() as client:
#         with app.app_context():  # New!!
#             assert current_app.config["ENV"] == "production"
#         yield client


# def test_index():
#     tester = app.test_client()
#     response = tester.get("/", content_type="html/text")

#     assert response.status_code == 200
#     # assert response.data == b"Hello, World!"


# def create_lobby(client):
#     client.post("lobby/create", json={"name": "mario"})
