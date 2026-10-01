import re
from flask import Flask, render_template, session, redirect, url_for, flash, request, jsonify
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)

app.config['SECRET_KEY'] = 'hard to guess string'


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    email = StringField('What is your UofT Email address?', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        old_email = session.get('email')
        if old_email is not None and old_email != form.email.data:
            flash('Looks like you have changed your email!')
        session['name'] = form.name.data
        if 'utoronto' in form.email.data:
            session['email'] = form.email.data
            return redirect(url_for('chat'))
        else:
            session['email'] = None
        return redirect(url_for('index'))
    return render_template('index.html',
        form = form, name = session.get('name'), email = session.get('email'))

@app.route('/chat', methods=['GET'])
def chat_page():
    return render_template('chat.html')


@app.route('/chat', methods=['POST'])
def chat():
    message = request.json['message']

    if message.lower().startswith('my name is '):
        name = message[11:].strip()
        session['chat_name'] = name
        reply = f'Nice to meet you, {name}!'

    elif 'what is my name' in message.lower():
        name = session.get('chat_name')

        if name:
            reply = f'Your name is {name}.'
        else:
            reply = "I don't know your name."

    elif 'hello' in message.lower():
        reply = 'Hello!'

    else:
        reply = "I don't understand."

    return {'reply': reply}


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))