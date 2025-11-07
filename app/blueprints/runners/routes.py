from flask import request, jsonify
from app.models import Runner, db, Team, Team_Runner_Role
from app.util.auth import encode_token, token_required
from .schemas import runner_schema, runners_schema, login_schema
from ..teams.schemas import team_schema, teams_schema
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from . import runners_bp
from sqlalchemy.orm import Session
# #Login
@runners_bp.route('/login', methods=['POST'])
def login():
    print("In login session ->")
    try:
        data = login_schema.load(request.json) #unpacking email and password
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    runner = db.session.query(Runner).where(Runner.email == data['email']).first() #checking if a runner belongs to this email

    if runner and check_password_hash(runner.password, data['password']): #If we found a runner with that email, then check that runners email against the email that was passed in
        token = encode_token(runner.id, runner.gender)
        return jsonify({
            "message": "Successfully logged in",
            "token": token,
            "runner": runner_schema.dump(runner)
        }), 200
    
    return jsonify({'error': 'invalid email or password'}), 404

# Create Runner
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

# #View Profile - Token Auth Teamually
@runners_bp.route('/<int:runner_id>', methods=['GET'])
def get_runner(runner_id):
    runner = db.session.get(Runner, runner_id)
    if runner: 
        return runner_schema.jsonify(runner), 200
    return jsonify({"error": "invalid runner id"}), 400

# #View All Runners
@runners_bp.route('', methods=['GET'])
def get_runners():
    runners = db.session.query(Runner).all()
    return runners_schema.jsonify(runners), 200

# #Update Profile
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

# #Delete Profile
@runners_bp.route('', methods=['DELETE'])
@token_required

def delete_runner():
    runner_id = request.runner_id

    runner = db.session.get(Runner, runner_id)
    if runner:
        db.session.delete(runner)
        db.session.commit()
        return jsonify({"message": "successfully deleted runner."}), 200
    return jsonify({"error": "invalid runner id"}), 404


#View My Invites
@runners_bp.route('/my-invites', methods=['GET'])
@token_required
def my_invites():
    return teams_schema.jsonify(db.session.get(Runner, request.runner_id).invites), 200

#ACCEPT INVITE
@runners_bp.route("/accept-invite/<int:team_id>", methods=['PUT']) 
@token_required
def accept_invite(team_id):

    runner = db.session.get(Runner, request.runner_id)
    team = db.session.get(Team, team_id)
    print(team)
    print(runner.invites)
    if runner and team:
        if team in runner.invites:
            team_runner_role = Team_Runner_Role(runner_id=runner.id, team_id=team.id, role = "member")
            db.session.add(team_runner_role)
            runner.invites.remove(team)
            db.session.commit()
            return jsonify({"message": f"Invite to {team.team_name} Accepted"}), 200
        else:
            return jsonify({"error": f"You are not invited to this team"}), 400
    else:
        return jsonify({"error": f"Invalid team_id"}), 400


#REJECT INVITE 
@runners_bp.route("/decline-invite/<int:team_id>", methods=['DELETE']) 
@token_required
def decline_invite(team_id):

    runner = db.session.get(Runner, request.runner_id)
    team = db.session.get(Team, team_id)

    if runner and team:
        if team in runner.invites:
            runner.invites.remove(team)
            db.session.commit()
            return jsonify({"message": f"Invite to {team.team_name} Declined."}), 200
        else:
            return jsonify({"error": f"You are not invited to this team."}), 400
    else:
        return jsonify({"error": f"Invalid team_id"}), 400
        
#ADD TO TEAM
@runners_bp.route("/add-to-team/<int:team_id>", methods=['POST']) 
@token_required
def add_to_team(team_id):

    runner = db.session.get(Runner, request.runner_id)
    team = db.session.get(Team, team_id)

    if runner and team:

        team_runner_role = Team_Runner_Role(runner_id=runner.id, team_id=team.id, role = "member")
        db.session.add(team_runner_role)
        db.session.commit()
        return jsonify({"message": f"Welcome to join {team.team_name}!"}), 200
    else:
        return jsonify({"error": f"Invalid team_id"}), 400