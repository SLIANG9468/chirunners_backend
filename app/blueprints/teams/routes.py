from flask import request, jsonify
from app.models import Team, db, Team_Runner_Role, Runner
from sqlalchemy.orm import Session
from app.util.auth import encode_token, token_required
from .schemas import team_schema, teams_schema, team_runner_role_schema, team_runner_roles_schema
from ..runners.schemas import runner_schema, runners_schema
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from . import teams_bp

#Create Team
@teams_bp.route('', methods=['POST'])
@token_required
def create_team():
    
    try:
        input_data = request.json
        if 'team_contact_id' not in input_data:
            input_data['team_contact_id']= request.runner_id
        data = team_schema.load(input_data)
        
        # Check if team name already exists
        existing_team = db.session.query(Team).where(Team.team_name == data['team_name']).first()
        if existing_team:
            return jsonify({'error': 'team_name already exist.'}), 400
        
        # Validate and create new team

        new_team = Team(**data)
        db.session.add(new_team)
        db.session.commit()  

    except ValidationError as e:
        return jsonify(e.messages), 400 

    return jsonify({
        "message": "successfully create team",
        "team": team_schema.dump(new_team)
    }), 201

#View Team Profile 
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
@token_required
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
@token_required
def delete_team(team_id):
    team = db.session.get(Team, team_id)
    if team:
        db.session.delete(team)
        db.session.commit()
        return jsonify({"message": "successfully deleted team."}), 200
    return jsonify({"error": "invalid team id"}), 404


# #View Team Runners
# @teams_bp.route('/<int:team_id>/runners', methods=['GET'])
# @token_required
# def team_runners(team_id):

#     with Session(db.engine) as session:
#         team = session.get(Team, team_id)
#         team_runners = session.query(Team_Runner_Role).filter_by(team_id=team_id).all()
#         return jsonify({"runners": team_runner_roles_schema.dump(team_runners),
#                         "team": team_schema.dump(team),
#                         "invited": runners_schema.dump(team.invites)}),200

    
#INVITE Runner
@teams_bp.route('/<int:team_id>/invite-runner/<int:runner_id>', methods=["PUT"])
@token_required
def invite_runner(team_id, runner_id):
    print("in right route")
    with Session(db.engine) as session:
        team = session.get(Team, team_id)
        runner = session.get(Runner, runner_id)
        print(runner)
        if team and runner:
            if runner not in team.invites:
                team.invites.append(runner)
                session.commit()
                return jsonify({"message": f"Successfully invited {runner.first_name}"})
            else:
                return jsonify({"Error": "runner already invited."}), 400
        else:
            return jsonify({"Error": "Invalid team_id or runner_id."}), 400
        
