from datetime import datetime
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from . import db, ma
from marshmallow import fields

class Plant(db.Model):
    """
        Class to define structure of table plant in DataBase.
    """
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

class WaterlevelData(db.Model):
    """
        Class to define structure of table waterlevel_data in DataBase.
    """
    id = db.Column(db.Integer, primary_key=True)
    plant_id = db.Column(db.Integer, db.ForeignKey('plant.id'), nullable=False)
    value = db.Column(db.Integer, nullable=False, default=2)
    report_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"Value('{self.plant_id}', '{self.value}', '{self.report_time}')"


class PlantSchema(SQLAlchemyAutoSchema):
    """
        Schema for plants. 
        JSON representation of the plant for the API and JavaScript.
    """
    class Meta:
        model = Plant
        sqla_session = db.session
        include_relationships = True
        load_instance = True

    values = fields.Nested("PlantValueSchema", default=[], many=True)


class PlantValueSchema(SQLAlchemyAutoSchema):
    """
        This class exists to get around a recursion issue

        It is not actually needed. Represents a plant object with one value, redundant due to PlantSchema.
    """
    id = fields.Int()
    plant_id = fields.Int()
    value = fields.Int()
    report_time = fields.DateTime()


class WaterlevelSchema(SQLAlchemyAutoSchema):
    """
        Schema for creating new values. 

        Parameter form as a python dictonary, like: {"plant_id": 0, "value": 5}
    """
    class Meta:
        model = WaterlevelData
        sqla_session = db.session
        include_relationships = True
        load_instance = True

    plant_id = fields.Int()

class ValuePlantSchema(ma.SQLAlchemyAutoSchema):
    """
        Schema for plants and all values combined.
        JSON representation of one plant object and all its values.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    plant_id = fields.Int()
    name = fields.Str()
    creation_date = fields.DateTime()
    last_update = fields.DateTime()
    image_file = fields.Str()
    min_fill_value = fields.Int()
    max_fill_value = fields.Int()
    values = fields.Nested("WaterlevelSchema", many=True)
    