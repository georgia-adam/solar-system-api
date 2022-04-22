from flask import Blueprint, jsonify

class Planet:
    def __init__(self, id, name, description, life):
        self.id = id
        self.name = name
        self.description = description
        self.life = life


planets = [
    Planet(1, "Earth", "Best planet", True),
    Planet(2, "Saturn", "Got a ring on it", False),
    Planet(3, "Mars", "We want to go there", False)
]

bp = Blueprint("planets_bp", __name__, url_prefix="/planets")

@bp.route("", methods=["GET"])
def get_planets():
    planets_list = []
    
    for planet in planets:
        planets_list.append({
            "id": planet.id,
            "name": planet.name,
            "description": planet.description,
            "life": planet.life
        })
    
    return jsonify(planets_list)
