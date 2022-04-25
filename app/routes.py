from flask import Blueprint, jsonify, abort, make_response

class Planet:
    def __init__(self, id, name, description, life):
        self.id = id
        self.name = name
        self.description = description
        self.life = life

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            description=self.description,
            life=self.life
        )


planets = [
    Planet(1, "Earth", "Best planet", True),
    Planet(2, "Saturn", "Got a ring on it", False),
    Planet(3, "Mars", "We want to go there", False)
]

bp = Blueprint("planets_bp", __name__, url_prefix="/planets")


def validate_planet(id):
    try:
        id = int(id)
    except:
        abort(make_response({"message":f"planet {id} invalid"}, 400))

    for planet in planets:
        if planet.id == id:
            return planet

    abort(make_response({"message":f"planet {id} not found"}, 404))


@bp.route("", methods=["GET"])
def get_planets():
    planets_list = []
    
    for planet in planets:
        planets_list.append(planet.to_dict())
    
    return jsonify(planets_list)

@bp.route("/<id>", methods=["GET"])
def get_one_planet(id):
    planet = validate_planet(id)
    return planet.to_dict()