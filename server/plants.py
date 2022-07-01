from datetime import datetime
from flask import make_response, abort
from .db_models import Plant, WaterlevelData, PlantSchema
from . import db, app


def read_all():
    """
    Lists all entries in table Plants. Used to list all plants in the main-page

    Query selects all entries in Table Plant ordered by id ascending
    
    data: PlantSchema is defined in module plants.py 
    It defines the json (?) representation of the Plant object so that AJAX can handle it and send data to the DOM
    """
    
    plants = Plant.query.order_by(Plant.id).all()#.join(WaterlevelData, Plant.id == WaterlevelData.plant_id).all()
    # apply the PlantSchema to return it as a json 
    plant_schema = PlantSchema(many=True)
    data = plant_schema.dump(plants)

    return data


def read_one(plant_id):
    """
        Used for single-page application to show only 1 plant in the highliter version
    """
    plant = Plant.query.filter(Plant.id == plant_id).one_or_none()

    if plant is not None:
        plant_schema = PlantSchema()
        data = plant_schema.dump(plant)
        return data
    else:
        abort(404, f"Plant {plant_id} not found.")

def create_plant(plant):
    """
        Create a new plant

        1. add new db item
        2. handle it somehow D:

        parameters: 
        1. name
        2. image_file (file name, optional [empty])
        3. max_fill_value (optional [empty])
    """
    p_name = plant.get("name")

    existing_plants = (Plant.query.filter(Plant.name == p_name).one_or_none())

    if existing_plants is None:
        schema = PlantSchema()
        new_plant = schema.load(plant, session=db.session)

        db.session.add(new_plant)
        db.session.commit()

        data = schema.dump(new_plant)

        return data, 201
    else:
        abort(409, f"Plant with name {p_name} already exists.")


def update(plant_id, updated_plant):
    """
        Manually update a plant
        Parameters:
            - plant_id: the plant to edit by its id
            - updated_plant: the new values of the plant 
    """
    plant = Plant.query.filter(Plant.id == plant_id).on_or_none()

    if plant is not None:
        pass # update plant entry in DataBase with new values from updated_plant object
    else:
        abort(404, f"Plant /w id {plant_id} could not be found.\nInternal Server Error!")
    pass

def delete(plant_id):
    """
        Delete a plant (whole deletion, as well in the db)
    """
    plant = Plant.query.filter(Plant.id == plant_id).one_or_none()

    if plant is not None:
        db.session.delete(plant)
        db.session.commit()

        return make_response(f"Plant with id {plant_id} deleted.", 200)
    else:
        abort(404, f"Plant with id {plant_id} not found.")