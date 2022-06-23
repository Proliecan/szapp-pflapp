from flask import render_template, redirect, url_for
from server.db_models import Plant, WaterlevelData
from server import app

# -----------------------------------------
# routes

# redirect to start-page 
@app.route('/')
def home():
    return redirect(url_for('start'), code=302)

# start-page
@app.route('/start')
def start():
    return render_template('index.html')

# imprint
@app.route('/imprint')
def imprint():
    return render_template('imprint.html')
