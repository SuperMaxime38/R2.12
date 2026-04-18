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
