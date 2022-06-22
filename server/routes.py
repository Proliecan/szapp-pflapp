from flask import render_template
from server.db_models import Plant, WaterlevelData
from server import app

# -----------------------------------------
# routes
# create basic route
@app.route('/')
def home():
    return render_template('index.html')


# route to imprint
@app.route('/imprint')
def imprint():
    return render_template('imprint.html')
