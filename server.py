from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import connexion
from datetime import datetime

# -----------------------------------------
# create server
connexion_app = connexion.App(__name__, specification_dir='./')


# -----------------------------------------
# configurations
# connexion_app.add_api('swagger.yml')

app = connexion_app.app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/plants.db'

db = SQLAlchemy(app)

# -----------------------------------------
# DataBase configuration 
# TODO: finish DB
# https://www.youtube.com/watch?v=cYWiDiIUxQc
# https://www.youtube.com/watch?v=44PvX0Yv368

class Plant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_update = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    image_file = db.Column(db.String(), unique=False, nullable=False, default='static/client/img/001-botanic.svg')
    values = db.relationship('WaterlevelData', backref='name', lazy=True)

    def __repr__(self) -> str:
        return f"Plant('{self.name}', '{self.creation_date}', '{self.last_update}', '{self.image_file}')"

class WaterlevelData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plant_id = db.Column(db.Integer, db.ForeignKey('plant.id'), nullable=False)
    value = db.Column(db.Integer, nullable=False, default=0.5)
    report_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"Plant('{self.value}', '{self.report_time}')"


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


if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)