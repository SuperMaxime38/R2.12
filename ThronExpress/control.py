from flask import Flask, render_template, url_for, request, redirect, session, jsonify
from .modele import *
import uuid,os
app = Flask(__name__)

# Config options - Make sure you created a 'config.py' file.
app.config.from_pyfile('config.py')

@app.route('/')
def index():
    isLogged = False
    if('ID' in session):
        isLogged = True

    return render_template('index.html', isLogged = isLogged)

@app.route('/search')
def search():
    # TODO
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    message = request.args.get('msg')
    if message is None:
        message = ""
    return render_template('login.html', msg = message)

@app.route('/login/submit', methods=['POST'])
def login_submit():

    user = log_in(request.form['username'], request.form['password'])
    if(len(user) != 0):
        session['ID'] = user[0][0]
        return redirect(url_for('index'))
    
    return redirect(url_for('login', msg = "Wrong username or password"))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    message = request.args.get('msg')
    if message is None:
        message = ""
    return render_template('signup.html', msg = message)

@app.route('/signup/submit', methods=['POST'])
def signup_submit():
    # TODO

    UUID = uuid.uuid4()
    if(addUser(UUID, request.form['username'], request.form['name'], request.form['phone'], request.form['password'])):
        session['ID'] = UUID
        return redirect(url_for('index'))

    return redirect(url_for('signup', msg = "An account si already associated with this phone number"))

@app.route('/account')
def account():
    # TODO
    return render_template('index.html')

@app.route('/about')
def about():
    # TODO
    return render_template('index.html')

@app.route('/subscribtions')
def subscribtions():
    # TODO
    return render_template('index.html')