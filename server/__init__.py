from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import connexion


# -----------------------------------------
# create server
connexion_app = connexion.App(__name__, specification_dir='./')


# -----------------------------------------
# configurations

app = connexion_app.app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/plants.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)

connexion_app.add_api('swagger.yml')

from server import routes