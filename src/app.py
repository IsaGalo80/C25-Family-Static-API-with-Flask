"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_all_member():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "family": members
    }
    return jsonify(response_body), 200

@app.route('/members/<int:id>', methods=['DELETE'])
def borrar_member(id):
    members = jackson_family.delete_member(id)
    return jsonify({"done":True}), 200

@app.route('/members/<int:id>', methods=['GET'])
def get_member(id):
    members = jackson_family.get_member(id)
    return jsonify({"done":True}), 200



@app.route('/members', methods=['POST'])
def crear_member_nuevo():
    nuevo_id=request.json.get("id")
    nuevo_age=request.json.get("age")
    nuevo_first_name=request.json.get("first_name")
    nuevo_last_name=request.json.get("last_name")
    nuevo_lucky_numbers=request.json.get("lucky_numbers")
    nuevo_member={
        "id":nuevo_id or jackson_family.generateId(),
        "first_name":nuevo_first_name,
        "last_name":nuevo_last_name,
        "age":nuevo_age,
        "lucky_numbers":nuevo_lucky_numbers,
    }
    jackson_family.add_member(nuevo_member)
    return jsonify({"done":True})

    # body = json.loads(request.data)
    # # this is how you can use the Family datastructure by calling its methods
    # members = jackson_family.crear_all_members()
    
    response_body = {
        "family": members
    }



    # return jsonify(response_body)
    return jsonify(_members), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)


