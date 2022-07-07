from flask import abort
from .db_models import Plant, WaterlevelData, WaterlevelSchema
from . import db


def read_all():
    """
        Read all values of one plant
    """
    values = WaterlevelData.query.order_by(db.desc(WaterlevelData.report_time)).all()

    if values is not None:
        values_schema = WaterlevelSchema(many=True, exclude=["plant.values"])
        data = values_schema.dump(values)
        return data
    else:
        abort(404, "Could not find any values.")


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


def add_new_value(water_value):
    """
        add new value to plant by id
    """
    existing_plants = (Plant.query.filter(Plant.id == water_value.get("plant_id")).one_or_none())
    print(existing_plants)

    if existing_plants is not None:
        schema = WaterlevelSchema()
        new_value = schema.load(water_value, session=db.session)

        db.session.add(new_value)
        db.session.commit()

        data = schema.dump(new_value)

        return data, 201
    else:
        abort(409, f"Plant with id {water_value.get('plant_id')} does not exist.")
