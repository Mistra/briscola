from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    '''
    This class implements a basic form to request for a Username and redirect the user to a game page
    '''
    username = StringField('Username', validators=[DataRequired()])
    play = SubmitField('Play')
    room = SubmitField(
        'Create Room'
    )  #This is a future feature. The idea is to let the user create a "private" session to share with his friends to play together.
