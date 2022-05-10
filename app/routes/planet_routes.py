from unicodedata import name
from app import db
from app.models.moon import Moon
from app.models.planet import Planet
from flask import Blueprint, jsonify, make_response, request
from .routes_helper import validate_planet, error_message


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
    
    name_param = request.args.get("name")

    if name_param:
        planets = Planet.query.filter_by(name=name_param)
    else:
        planets = Planet.query.all()
    
    planets_response = [planet.to_dict() for planet in planets]
    
    return jsonify(planets_response), 200


@planets_bp.route("/<planet_id>", methods=["GET"])
def get_planet_by_id(planet_id):
    
    planet = validate_planet(planet_id)
    
    return jsonify(planet.to_dict()), 200

@planets_bp.route("/<planet_id>", methods=["PUT"])
def replace_planet(planet_id):
    planet = validate_planet(planet_id)
    request_body = request.get_json()
    
    try:
        planet.name = request_body["name"]
        planet.description = request_body["description"]
        planet.has_life = request_body["has_life"]
    except KeyError as err:
        error_message(f"Missing key {err}", 400)

    db.session.commit()
    return make_response(f"Planet {planet_id} successfully updated!", 200)

@planets_bp.route("/<planet_id>", methods=["DELETE"])
def delete_planet(planet_id):
    planet = validate_planet(planet_id)

    db.session.delete(planet)
    db.session.commit()
    return make_response(f"Planet {planet_id} successfully deleted.")

@planets_bp.route("/<planet_id>/moons", methods=["POST"])
def add_moon_to_planet(planet_id):
    
    planet = validate_planet(planet_id)
    request_body = request.get_json()
    new_moon = Moon(name=request_body['name'])
    new_moon.planet = planet

    db.session.add(new_moon)
    db.session.commit()

    return jsonify(new_moon.to_dict()), 201

@planets_bp.route("/<planet_id>/moons", methods=["GET"])
def get_all_moon_of_a_planet(planet_id):
    
    planet = validate_planet(planet_id)
    moons_info = [moon.to_dict() for moon in planet.moons]

    return jsonify(moons_info)