from datetime import datetime
from xml.etree.ElementInclude import include

from marshmallow_sqlalchemy import auto_field
from sqlalchemy import values
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

# class WaterlevelSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = WaterlevelData
#         include_fk = True
#         load_instance = True

#     plant = fields.Nested(PlantValueSchema, default=None)

# class PlantSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = Plant
#         load_instance = True

#     values = fields.Nested(WaterlevelSchema, many=True)
#     # WaterlevelData.last_value = auto_field()

# class PlantValueSchema(ma.ModelSchema):
#     # class Meta:
#     #     model = Plant
#     #     load_instance = True

#     # value = fields.List(WaterlevelSchema, many=True)
#     def __init__(self, **kwargs):
#         super().__init__(strict=True, **kwargs)

#     value_id = fields.Int()
#     plant_id = fields.Int()
#     value = fields.Str()
#     timestamp = fields.Str()


class PlantSchema(ma.SQLAlchemyAutoSchema):
    # def __init__(self, **kwargs):
    #     super().__init__(strict=True, **kwargs)

    class Meta:
        model = Plant
        sqla_session = db.session

    values = fields.Nested("PlantValueSchema", default=[], many=True)


class PlantValueSchema(ma.SQLAlchemyAutoSchema):
    """
    This class exists to get around a recursion issue
    """

    # def __init__(self, **kwargs):
    #     super().__init__(strict=True, **kwargs)

    value_id = fields.Int()
    plant_id = fields.Int()
    value = fields.Int()
    report_time = fields.DateTime()


class WaterlevelSchema(ma.SQLAlchemyAutoSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = WaterlevelData
        sqla_session = db.session

class ValuePlantSchema(ma.SQLAlchemyAutoSchema):
    """
    This class exists to get around a recursion issue
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
    