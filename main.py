from flask import Flask, render_template, url_for, request, redirect, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dateutil import tz
import matplotlib.pyplot as plt
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

def create_graph(t_humidity, t_plant, id):
    graph_path = r'/var/www/sap-pflapp/static/client/img/graph.png' # location on RaspberryPi
    
    # delete old graph
    if os.path.exists(graph_path):
        os.remove(graph_path)

    # fetch data
    humidity_data = [getattr(r, 'humidity') for r in t_humidity if getattr(r, 'pID') == id]
    date_data = [getattr(r, 'date_time') for r in t_humidity if getattr(r, 'pID') == id]


    # create new graph
    plt.style.use('ggplot')
    
    plt.title(f'graph für Pflanze {t_plant.name}', fontsize=16)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Feuchtigkeit in %', fontsize=12)

    plt.plot(date_data, humidity_data, color='green')

    plt.savefig(graph_path)
    plt.switch_backend('agg')
    plt.clf()

# class for table Plants 
class Plants(db.Model):
    __tablename__ = 'Plants'
    pId = db.Column(db.Integer, primary_key=True)
    room = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    species = db.Column(db.String(200), nullable=False)

    def __repr__(self) -> str:
        return f"<Plant {self.name}"

# class for table humidity
class Humidity(db.Model):
    __tablename__ = 'humidity'
    pID = db.Column(db.Integer, primary_key=True)
    date_time = db.Column(db.String(200), nullable=False, primary_key=True)
    humidity = db.Column(db.Integer, primary_key=True)

    def __repr__(self) -> str:
        return f"<Plant {self.pID}>"

# Index
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        return "Hello"
    else:
        plants = Plants.query.order_by(Plants.name).all()
        return render_template('index.html', plants=plants)

# show Plant info
@app.route('/plant_info/<int:pId>')
def show_details(pId):
    plant = Plants.query.get(pId)
    humidity = Humidity.query.filter(Humidity.pID==pId).order_by(Humidity.date_time.asc())

    create_graph(humidity, plant, pId)

    humidity = Humidity.query.filter(Humidity.pID==pId).order_by(Humidity.date_time.desc()).first()

    return render_template('plant_info.html', plant=plant, humidity=humidity, id=pId)


@app.template_filter()
def convert_date(date):
    date_object = datetime.strptime(date, '%Y-%m-%d %X').replace(tzinfo=tz.tzutc())
    date_object = date_object.astimezone(tz.tzlocal())
    return datetime.strftime(date_object, format="%X %d.%m.%Y")


if __name__ == "__main__":
    app.run(debug=True)
