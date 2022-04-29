from app import db
from app.models.planet import Planet
from flask import Blueprint, jsonify, make_response, request


planets_bp = Blueprint("planets", __name__, url_prefix="/planets")

@planets_bp.route("", methods=["POST"])
def create_planet():
    request_body = request.get_json()
    
    planet = Planet(
        name=request_body["name"],
        description=request_body["description"],
        has_life=request_body["has_life"])

    db.session.add(planet)
    db.session.commit() 

    return jsonify(planet.to_dict()), 201


@planets_bp.route("", methods=["GET"])
def get_planets():
    planets = Planet.query.all()
    
    planets_response = [planet.to_dict() for planet in planets]
    
    return jsonify(planets_response)

# ----old code not yet refactored----
# def validate_planet(id):
#     try:
#         id = int(id)
#     except:
#         abort(make_response({"message":f"planet {id} invalid"}, 400))

#     for planet in planets:
#         if planet.id == id:
#             return planet

#     abort(make_response({"message":f"planet {id} not found"}, 404))


# @bp.route("/<id>", methods=["GET"])
# def get_one_planet(id):
#     planet = validate_planet(id)
#     return planet.to_dict()