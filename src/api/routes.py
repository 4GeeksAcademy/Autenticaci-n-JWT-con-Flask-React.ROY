"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from sqlalchemy import select
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

@api.route('/signup', methods=['POST'])
def register():
    try:
        data = request.json

        if not data['email'] or not data['password']:
            raise Exception({"error":'missing data'})
        stm = select(User).where(User.email == data['email'])
        user_existing = db.session.execute(stm).scalar_one_or_none()
        if user_existing:
            raise Exception({"error":'existing email,try to log-in'})
        newUser = User (
            email = data['email'],
            password = data['password'],
            is_active = True            
        )
        db.session.add(newUser)
        db.session.commit()

        token = create_access_token(identity=str(newUser.id))
        return jsonify({"msg":"sing-in up success","token":token}),201

    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({"error":'something went wrong'}),400
    

@api.route('/login', methods=['POST'])
def login():
    try:
        data = request.json

        if not data['email'] or not data['password']:
            raise Exception({"error":'missing data'})
        stm = select(User).where(User.email == data['email'])
        user = db.session.execute(stm).scalar_one_or_none()
        if not user:
            raise Exception({"error":'email not found,please register'})
        if (user.password != data['password']):
            raise Exception({"error":'Wrong email or password'})
        
        token = create_access_token(identity=str(user.id))
        return jsonify({"msg":"login success","token":token}),200

    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({"error":'something went wrong'}),400
    

@api.route('/private', methods= ['GET'])
@jwt_required()
def getUserinfo():
    try:
        id= get_jwt_identity()
        
        stm = select(User).where(User.id == id)
        user = db.session.execute(stm).scalar_one_or_none()
        if not user:
            return jsonify ({"error":"no information for this user"}),418

        return jsonify(user.serialize())
    except Exception as e :
        print(e)
        return jsonify({"msg", ""})