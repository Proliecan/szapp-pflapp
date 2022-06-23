from datetime import datetime
from flask import make_response, abort

# -----------------------------------------
# temporary plants data until db

PLANTS = {
    "P-0001" : {
        "name" : "Bertha",
        "id" : 1,
        "creation-date" : datetime.now().strftime(("%Y-%m-%d %H:%M:%S")),
        "last-update" : datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))
    },
    "P-0002" : {
        "name" : "Karla",
        "id" : 2,
        "creation-date" : datetime.now().strftime(("%Y-%m-%d %H:%M:%S")),
        "last-update" : datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))
    },
}

PLANTS_DATA = {
    "0001" : {
        "id" : 1,
        "plant-id" : 1,
        "value" : 0.56, # waterlevel
        "time" : datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))
    },
    "0002" : {
        "id" : 2,
        "plant-id" : 2,
        "value" : 0.75, # waterlevel
        "time" : datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))
    },
    "0003" : {
        "id" : 3,
        "plant-id" : 1,
        "value" : 0.56, # waterlevel
        "time" : datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))
    },
    "0004" : {
        "id" : 4,
        "plant-id" : 2,
        "value" : 0.7, # waterlevel
        "time" : datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))
    }
}

# -----------------------------------------

def read_all():
    """
        Used to list all plants in the main-page
    """
    pass

def read_one():
    """
        Used for single-page application to show only 1 plant in the highliter version
    """
    pass

def create_plant():
    """
        Create a new plant

        1. add new db item
        2. handle it somehow D:
    """
    pass

def update():
    """
        Manually update a plant
    """
    pass

def delete():
    """
        Delete a plant (whole deletion, as well in the db)
    """
    pass