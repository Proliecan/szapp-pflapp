from datetime import datetime
from flask import make_response, abort
from .db_models import Plant, WaterlevelData, PlantSchema
from . import db, app
 
def read_all(plant_id):
    """
        Read all values of one plant
    """
    pass
 
def read_last(plant_id):
    """
        Read last value of a plant
    """
    pass
 
def delete_all(plant_id):
    """
        Delete all values of one plant
    """
    pass
 
def add_new_value(plant_id, WaterlevelData):
    """
        add a new value to a plant
    """
    pass
