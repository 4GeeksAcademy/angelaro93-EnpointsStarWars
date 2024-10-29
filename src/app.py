"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Fav
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def get_all_users():
    users = User.query.all()  # Obtener todos los registros de User
    users_list = [user.serialize() for user in users]  # Serializar cada registro
    return jsonify(users_list), 200

@app.route('/user/<int:id>/favs', methods=['GET'])
def get_users_favs(id):
    user = User.query.get(id)  # Obtener todos los registros de User
    favs = [fav.serialize() for fav in user.favs]  # Serializar cada registro
    return jsonify(favs), 200


@app.route('/character', methods=['GET'])
def get_all_characters():
    characters = Character.query.all()  
    characters_list = [character.serialize() for character in characters]  
    return jsonify(characters_list), 200

@app.route('/character/<int:character_id>', methods=['GET'])
def get_character(character_id):
    character = Character.query.get(character_id)
    if character is None:
        raise APIException('Character not found', status_code=404)
    return jsonify(character.serialize()), 200


@app.route('/favorite/character/<int:character_id>', methods=['POST'])
def add_favorite_character(character_id):
    user_id = request.json.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Verificar si el personaje ya está en favoritos
    existing_fav = Fav.query.filter_by(id_user=user_id, id_character=character_id).first()
    if existing_fav:
        return jsonify({"error": "Character already in favorites"}), 400

    # Agrega el personaje como favorito
    new_fav = Fav(id_user=user_id, id_character=character_id)
    db.session.add(new_fav)
    db.session.commit()
    return jsonify(new_fav.serialize()), 201


@app.route('/favorite/character/<int:character_id>', methods=['DELETE'])
def remove_favorite_character(character_id):
    user_id = request.json.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Eliminar el personaje de los favoritos si existe
    fav = Fav.query.filter_by(id_user=user_id, id_character=character_id).first()
    if not fav:
        return jsonify({"error": "Character not found in favorites"}), 404

    db.session.delete(fav)
    db.session.commit()
    return jsonify({"message": "Character removed from favorites"}), 200


@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planet.query.all()  
    planets_list = [planet.serialize() for planet in planets]  
    return jsonify(planets_list), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet is None:
        raise APIException('Planet not found', status_code=404)
    return jsonify(planet.serialize()), 200

@app.route('/favorite/planet', methods=['POST'])
def add_favorite_planet():
    user_id = request.json.get("user_id")
    planet_id = request.json.get("planet_id")
    if not user_id or not planet_id:
        return jsonify({"Error": "user_id and planet_id are required"}), 400
    user = User.query.get(user_id)
    if not user:
        return jsonify({"Error": "User not found"}), 404
    existing_fav = Fav.query.filter_by(id_user=user_id, id_planet=planet_id).first()
    if existing_fav:
        return jsonify({"Error": "Planet already in favorites"}), 400
   
    new_fav = Fav(id_user=user_id, id_planet=planet_id)
    db.session.add(new_fav)
    db.session.commit()
    return jsonify(new_fav.serialize()), 201


@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def remove_favorite_planet(planet_id):
    user_id = request.json.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    fav = Fav.query.filter_by(id_user=user_id, id_planet=planet_id).first()
    if not fav:
        return jsonify({"error": "Planet not found in favorites"}), 404

    db.session.delete(fav)
    db.session.commit()
    return jsonify({"message": "Planet removed from favorites"}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
