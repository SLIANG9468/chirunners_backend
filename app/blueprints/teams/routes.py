from flask import request, jsonify
from app.models import Team, db
from .schemas import team_schema, teams_schema
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from . import teams_bp

#Login

#Register/Create Team
@teams_bp.route('', methods=['POST'])
def create_team():
    #load validata the request data
    try:
        data = team_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400 
    
    team = db.session.query(Team).where(Team.team_name == data['team_name']).first() #Checking if a team exist in my db who has the same password as the one passed in
    if team:
        return jsonify({'error': 'team_name already exist.'}), 400
    
    new_team = Team(**data) #Create new team
    db.session.add(new_team)
    db.session.commit()
    #create a new Team in my database

    #send a response
    return jsonify({
        "message": "successfully create team",
        "team": team_schema.dump(new_team)
    }), 201

#View Profile - Token Auth Eventually
@teams_bp.route('/<int:team_id>', methods=['GET'])
def get_team(team_id):
    team = db.session.get(Team, team_id)
    if team: 
        return team_schema.jsonify(team), 200
    return jsonify({"error": "invalid team id"}), 400

#View All Teams
@teams_bp.route('', methods=['GET'])
def get_teams():
    teams = db.session.query(Team).all()
    return teams_schema.jsonify(teams), 200

#Update Profile
@teams_bp.route('/<int:team_id>', methods=['PUT'])

def update_team(team_id):

    team = db.session.get(Team,team_id)

    if not team:
        return jsonify({"error": "Invalid Team Id"}), 404
    
    try:
        data = team_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    for key, value in data.items():
        setattr(team, key, value)

    db.session.commit()
    return jsonify({
        "message": "successfully upadated account",
        "team": team_schema.dump(team)
    }), 200

#Delete Profile
@teams_bp.route('/<int:team_id>', methods=['DELETE'])
def delete_team(team_id):
    team = db.session.get(Team, team_id)
    if team:
        db.session.delete(team)
        db.session.commit()
        return jsonify({"message": "successfully deleted team."}), 200
    return jsonify({"error": "invalid team id"}), 404