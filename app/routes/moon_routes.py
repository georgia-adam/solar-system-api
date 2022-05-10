from unicodedata import name
from app import db
from app.models.moon import Moon
from flask import Blueprint, jsonify, make_response, request
from .routes_helper import validate_moon, error_message


moons_bp = Blueprint("moons", __name__, url_prefix="/moons")

@moons_bp.route("", methods=["POST"])
def create_moon():
    request_body = request.get_json()
    
    moon = Moon(
        name=request_body["name"])

    db.session.add(moon)
    db.session.commit() 

    return jsonify(moon.to_dict()), 201


@moons_bp.route("", methods=["GET"])
def get_moons():
    
    name_param = request.args.get("name")

    if name_param:
        moons = Moon.query.filter_by(name=name_param)
    else:
        moons = Moon.query.all()
    
    moons_response = [moon.to_dict() for moon in moons]
    
    return jsonify(moons_response), 200


@moons_bp.route("/<moon_id>", methods=["GET"])
def get_moon_by_id(moon_id):
    
    moon = validate_moon(moon_id)
    
    return jsonify(moon.to_dict()), 200

@moons_bp.route("/<moon_id>", methods=["PUT"])
def replace_moon(moon_id):
    moon = validate_moon(moon_id)
    request_body = request.get_json()
    
    try:
        moon.name = request_body["name"]
        moon.description = request_body["description"]
        moon.has_life = request_body["has_life"]
    except KeyError as err:
        error_message(f"Missing key {err}", 400)

    db.session.commit()
    return make_response(f"moon {moon_id} successfully updated!", 200)

@moons_bp.route("/<moon_id>", methods=["DELETE"])
def delete_moon(moon_id):
    moon = validate_moon(moon_id)

    db.session.delete(moon)
    db.session.commit()
    return make_response(f"moon {moon_id} successfully deleted.")
