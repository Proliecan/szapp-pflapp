from datetime import datetime
from flask import make_response, abort
from .db_models import Plant, WaterlevelData, PlantSchema, WaterlevelSchema
from . import db, app
 
def read_all():
    """
        Read all values of one plant
    """
    values = WaterlevelData.query.order_by(db.desc(WaterlevelData.report_time)).all()

    values_schema = WaterlevelSchema(many=True, exclude=["plant.values"])
    data = values_schema.dump(values)
    return data
 
def read_last(plant_id):
    """
        Read last value of a plant
    """
    value = WaterlevelData.query.join(Plant, Plant.id == WaterlevelData.plant_id).filter(Plant.id == plant_id).order_by(db.desc(WaterlevelData.report_time)).one_or_none()

    if value is not None:
        value_schema = WaterlevelSchema()
        data = value_schema.dump(value)
        return data
    else:
        abort(404, f"Last value for plant {plant_id} not found.")
 
def delete_all(plant_id):
    """
        Delete all values of one plant
    """
    pass
 
def add_new_value(plant_id, new_value):
    """
        Create a new plant

        1. add new db item
        2. handle it somehow D:

        parameters: 
        1. name
        2. image_file (file name, optional [empty])
        3. max_fill_value (optional [empty])
    """
    existing_plants = (Plant.query.filter(Plant.id == plant_id).one_or_none())
    print(existing_plants)

    if existing_plants is not None:
        schema = WaterlevelSchema()
        new_value = schema.load(new_value, session=db.session)

        db.session.add(new_value)
        db.session.commit()

        data = schema.dump(new_value)

        return data, 201
    else:
        abort(409, f"Plant with id {plant_id} does not exist.")
