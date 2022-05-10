from flask import jsonify, make_response, abort
from app.models.planet import Planet
from app.models.moon import Moon

def error_message(message, status_code):
    abort(make_response(message, status_code))

def validate_planet(id):
    try:
        id = int(id)
    except:
        error_message({"message":f"planet {id} invalid"}, 400)

    planet = Planet.query.get(id)

    if not planet:
        error_message({"message":f"planet {id} not found"}, 404)
    else:
        return planet

def validate_moon(id):
    try:
        id = int(id)
    except:
        error_message({"message":f"moon {id} invalid"}, 400)

    moon = Moon.query.get(id)

    if not moon:
        error_message({"message":f"moon {id} not found"}, 404)
    else:
        return moon

