from flask import request, jsonify
from app.models import Runner, db
from app.util.auth import encode_token, token_required
from .schemas import runner_schema, runners_schema, login_schema
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from . import runners_bp

#Login
@runners_bp.route('/login', methods=['POST'])
def login():
    print("In login session ->")
    try:
        data = login_schema.load(request.json) #unpacking email and password
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    runner = db.session.query(Runner).where(Runner.email == data['email']).first() #checking if a runner belongs to this email

    if runner and check_password_hash(runner.password, data['password']): #If we found a runner with that email, then check that runners email against the email that was passed in
        token = encode_token(runner.id, runner.role)
        return jsonify({
            "message": "Successfully logged in",
            "token": token,
            "runner": runner_schema.dump(runner)
        }), 200
    
    return jsonify({'error': 'invalid email or password'}), 404

#Register/Create Runner
@runners_bp.route('', methods=['POST'])
def create_runner():
    #load validata the request data
    try:
        data = runner_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400 
    
    data['password'] = generate_password_hash(data['password']) #Reassigning the password to the hashed version of the pw

    runner = db.session.query(Runner).where(Runner.email == data['email']).first() #Checking if a runner exist in my db who has the same password as the one passed in
    if runner:
        return jsonify({'error': 'Email already taken.'}), 400
    
    new_runner = Runner(**data) #Create new runner
    db.session.add(new_runner)
    db.session.commit()
    #create a new Runner in my database

    #send a response
    return jsonify({
        "message": "successfully create runner",
        "runner": runner_schema.dump(new_runner)
    }), 201

#View Profile - Token Auth Eventually
@runners_bp.route('/<int:runner_id>', methods=['GET'])
def get_runner(runner_id):
    runner = db.session.get(Runner, runner_id)
    if runner: 
        return runner_schema.jsonify(runner), 200
    return jsonify({"error": "invalid runner id"}), 400

#View All Runners
@runners_bp.route('', methods=['GET'])
def get_runners():
    runners = db.session.query(Runner).all()
    return runners_schema.jsonify(runners), 200

#Update Profile
@runners_bp.route('', methods=['PUT'])
@token_required

def update_runner():

    runner_id = request.runner_id

    runner = db.session.get(Runner,runner_id)

    if not runner:
        return jsonify({"error": "Invalid Runner Id"}), 404
    
    try:
        data = runner_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    data['password'] = generate_password_hash(data['password'])

    for key, value in data.items():
        setattr(runner, key, value)

    db.session.commit()
    return jsonify({
        "message": "successfully upadated account",
        "runner": runner_schema.dump(runner)
    }), 200

#Delete Profile
@runners_bp.route('/<int:runner_id>', methods=['DELETE'])
@token_required

def delete_runner():
    runner_id = request.runner_id

    runner = db.session.get(Runner, runner_id)
    if runner:
        db.session.delete(runner)
        db.session.commit()
        return jsonify({"message": "successfully deleted runner."}), 200
    return jsonify({"error": "invalid runner id"}), 404