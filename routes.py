from briscola import app
from flask import render_template, flash, redirect, url_for
from briscola.forms import LoginForm


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}'.format(form.username.data))
        return redirect(url_for('game'))
    return render_template('index.html', title='card game', form=form)


@app.route('/game')
def game():
    return "Hello"
    #return render_template('game.html', title='card game')
