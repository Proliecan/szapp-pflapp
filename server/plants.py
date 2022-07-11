from flask import make_response, abort
from .db_models import Plant, WaterlevelData, PlantSchema, ValuePlantSchema
from . import db
from .water_values import delete_all


def read_all():
    """
        Returns all plants in one object.
    """
    plants = Plant.query.order_by(Plant.id).all()

    if plants is not None:
        plant_schema = PlantSchema(many=True)
        data = plant_schema.dump(plants)

        return data
    else:
        abort(404, "No plants found.")


def read_one(plant_id):
    """
        Used for single-page application to show only 1 plant in the highliter version
    """
    plant = Plant.query.filter(Plant.id == plant_id).outerjoin(WaterlevelData).one_or_none()

    if plant is not None:
        plant_schema = ValuePlantSchema(many=False)
        data = plant_schema.dump(plant)

        # sort data by report time
        data['values'] = sorted(data['values'], key=lambda d: d['report_time'], reverse=False)

        return data
    else:
        abort(404, f"Plant {plant_id} not found.")


def create_plant(plant):
    """
        Create a new plant. Unique identifier is its id and name.
    """
    p_name = plant.get("name")

    existing_plant = Plant.query.filter(Plant.name == p_name).one_or_none()

    if existing_plant is None:
        print("here")

        schema = PlantSchema()
        new_plant = schema.load(plant, session=db.session)

        db.session.add(new_plant)
        db.session.commit()

        data = schema.dump(new_plant)

        return data, 201
    else:
        abort(409, f"Plant with name {p_name} already exists.")


def update(plant_id, new_plant):
    """
        Update a plant by its id. 
    """
    old_plant = Plant.query.filter(Plant.id == plant_id).one_or_none()
    
    p_name = new_plant.get("name")

    existing_plant = Plant.query.filter(Plant.name == p_name, Plant.id != plant_id).one_or_none()

    if existing_plant is None and old_plant is not None:
        schema = PlantSchema()
        update = schema.load(new_plant, session=db.session)

        update.id = old_plant.id

        db.session.merge(update)
        db.session.commit()

        data = schema.dump(update)

        return data, 200
    else:
        abort(404, f"Plant with id {plant_id} could not be found.\nInternal Server Error!")


def delete(plant_id):
    """
        Delete a plant (whole deletion, as well in the db)
    """
    plant = Plant.query.filter(Plant.id == plant_id).one_or_none()

    if plant is not None:
        delete_all(plant_id)

        db.session.delete(plant)
        db.session.commit()

        return make_response(f"Plant with id {plant_id} deleted.", 200)
    else:
        abort(409, f"Plant with id {plant_id} not found.")