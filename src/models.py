from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True, nullable=False)
    address = db.Column(db.String(50)) 
    phone = db.Column(db.String(50)) 
    date = db.Column(db.Date())

    favs = db.relationship("Fav", back_populates="user")
    

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            "address": self.address,
            "phone": self.phone,
            "date": self.date,
            "favs": [fav.serialize() for fav in self.favs]
        }


class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)  
    description = db.Column(db.String(200), nullable=True)

    favs = db.relationship("Fav", back_populates="planet")

    def __repr__(self):
        return '<PlanetAngela %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
        }


class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)  
    description = db.Column(db.String(200), nullable=True) 

    favs = db.relationship("Fav", back_populates="character")

    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
        }

    
class Fav(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    id_character = db.Column(db.Integer, db.ForeignKey('character.id'))
    id_planet = db.Column(db.Integer, db.ForeignKey('planet.id'))

    user = db.relationship("User", back_populates="favs")
    character = db.relationship("Character", back_populates="favs")
    planet = db.relationship("Planet", back_populates="favs")


    def __repr__(self):
        return '<Fav %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "id_user": self.id_user,
            "id_character": self.id_character,
            "id_planet": self.id_planet,
        }


            # do not serialize the password, its a security breach
        