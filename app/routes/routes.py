from unicodedata import name
from app import db
from app.models.planet import Planet
from flask import Blueprint, jsonify, make_response, request, abort


planets_bp = Blueprint("planets", __name__, url_prefix="/planets")

def validate_planet(id):
    try:
        id = int(id)
    except:
        abort(make_response({"message":f"planet {id} invalid"}, 400))

    planet = Planet.query.get(id)

    if not planet:
        abort(make_response({"message":f"planet {id} not found"}, 404))
    else:
        return planet

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

@planets_bp.route("/<planet_id>", methods=["PUT"])
def replace_planet(planet_id):
    planet = validate_planet(planet_id)
    request_body = request.get_json()
    
    try:
        planet.name = request_body["name"]
        planet.description = request_body["description"]
        planet.has_life = request_body["has_life"]
    except KeyError:
        return make_response("Key Error", 400)

    db.session.commit()
    return make_response(f"Planet {planet_id} successfully updated!", 200)

@planets_bp.route("/<planet_id>", methods=["DELETE"])
def delete_planet(planet_id):
    planet = validate_planet(planet_id)

    db.session.delete(planet)
    db.session.commit()
    return make_response(f"Planet {planet_id} successfully deleted.")
