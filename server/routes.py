from flask import render_template, redirect, url_for
from .db_models import Plant, WaterlevelData
from . import app

# -----------------------------------------
# routes

# redirect to start-page 
@app.route('/')
def home():
    return redirect(url_for('start'), code=302)

# start-page
@app.route('/start', methods=['GET'])
def start():
    return render_template('index.html')

# imprint
@app.route('/imprint', methods=['GET'])
def imprint():
    return render_template('imprint.html')

# route to add a new plant
@app.route('/add_plant')
def add_plant():
    return render_template('add_plant.html')

@app.route('/main_page', methods=['GET'])
def main_page():
    return render_template('main_page.html')