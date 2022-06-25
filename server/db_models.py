from datetime import datetime

from marshmallow_sqlalchemy import auto_field
from . import db, ma
from marshmallow import fields

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
    image_file = db.Column(db.String(), unique=False, nullable=False, default='static/img/001-botanic.svg')
    min_fill_value = db.Column(db.Integer, unique=False, nullable=False, default=0)
    max_fill_value = db.Column(db.Integer, unique=False, nullable=False, default=5)
    values = db.relationship('WaterlevelData', backref='name', lazy='joined')

    def __repr__(self) -> str:
        return f"{self.__dict__}"
        # return f"Plant('{self.name}', '{self.creation_date}', '{self.last_update}', '{self.image_file}')"

class WaterlevelData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plant_id = db.Column(db.Integer, db.ForeignKey('plant.id'), nullable=False)
    value = db.Column(db.Integer, nullable=False, default=2)
    report_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"Value('{self.plant_id}', '{self.value}', '{self.report_time}')"

class WaterlevelSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = WaterlevelData
        load_instance = True

class PlantSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Plant
        load_instance = True

    values = fields.Nested(WaterlevelSchema, many=True)
    # WaterlevelData.last_value = auto_field()
