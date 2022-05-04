from flask import jsonify, make_response, abort
from app.models.planet import Planet

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

