#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        """Retrieve all plants as JSON."""
        plants = Plant.query.all()
        return [plant.to_dict() for plant in plants], 200  

    def post(self):
        """Create a new plant entry."""
        data = request.get_json()

        if not data.get("name") or not data.get("image") or not data.get("price"):
            return {"error": "Missing required fields"}, 400

        try:
            new_plant = Plant(
                name=data["name"],
                image=data["image"],
                price=data["price"]
            )

            db.session.add(new_plant)
            db.session.commit()

            return new_plant.to_dict(), 201  
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500

class PlantByID(Resource):
     def get(self, id):
        """Retrieve a plant by ID."""
        plant = Plant.query.get(id)
        if plant:
            return plant.to_dict(), 200
        return {"error": "Plant not found"}, 404

api.add_resource(Plants, "/plants")
api.add_resource(PlantByID, "/plants/<int:id>")
        

if __name__ == '__main__':
    app.run(port=5555, debug=True)
