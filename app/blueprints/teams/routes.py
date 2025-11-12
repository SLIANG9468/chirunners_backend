from flask import request, jsonify
from app.models import Team, db, Team_Runner_Role, Runner
from app.util.auth import encode_token, token_required
from .schemas import team_schema, teams_schema, team_runner_role_schema, team_runner_roles_schema
from ..runners.schemas import runner_schema, runners_schema
from marshmallow import ValidationError
from . import teams_bp

#Create Team
@teams_bp.route('', methods=['POST'])
@token_required
def create_team():
    
    try:
        input_data = request.json
        is_creator = 'team_contact_id' not in input_data

        if is_creator:
            input_data['team_contact_id']= request.runner_id
        data = team_schema.load(input_data)
        
        existing_team = db.session.query(Team).where(Team.team_name == data['team_name']).first()
        if existing_team:
            return jsonify({'error': 'team_name already exist.'}), 400

        new_team = Team(**data)
        db.session.add(new_team)
        db.session.flush()  
        if is_creator:
            new_team_runner_role = Team_Runner_Role(
                team_id = new_team.id,
                runner_id = request.runner_id,
                role = 'member'
            )
            db.session.add(new_team_runner_role)
        
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
        "message": "successfully updated account",
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

#My Team
@teams_bp.route('/my-teams', methods=['GET'])
@token_required
def get_my_teams():
    my_teams = db.session.query(Team).join(Team_Runner_Role).filter_by(runner_id = request.runner_id).all()
    return jsonify(teams_schema.dump(my_teams)), 200

#View Team Runners
@teams_bp.route('/<int:team_id>/runners', methods=['GET'])
@token_required
def team_runners(team_id):

        team = db.session.get(Team, team_id)

        if not team:
            return jsonify({"error": "Invalid team id"}), 404

        team_runners = db.session.query(Team_Runner_Role).filter_by(team_id=team_id).all()
        return jsonify({"runners": team_runner_roles_schema.dump(team_runners),
                        "team": team_schema.dump(team),
                        "invited": runners_schema.dump(team.invites)}),200

#View My first Team's Runners
@teams_bp.route('/runners', methods=['GET'])
@token_required
def myteam_runners():

        my_team = db.session.query(Team_Runner_Role).filter_by(runner_id = request.runner_id).first()
        
        if not my_team:
            return jsonify({"error": "You are not a member of any team"}), 404
            
        team_runners = db.session.query(Team_Runner_Role).filter_by(team_id = my_team.team_id).all()
        return jsonify({"runners": team_runner_roles_schema.dump(team_runners),
                        "team": team_schema.dump(my_team.team)}), 200

    
#INVITE Runner
@teams_bp.route('/<int:team_id>/invite-runner/<int:runner_id>', methods=["PUT"])
@token_required
def invite_runner(team_id, runner_id):
    print("in right route")
    team = db.session.get(Team, team_id)
    runner = db.session.get(Runner, runner_id)
    print(runner)
    if team and runner:
        if runner not in team.invites:
            team.invites.append(runner)
            db.session.commit()
            return jsonify({"message": f"Successfully invited {runner.first_name}"}), 200
        else:
            return jsonify({"Error": "runner already invited."}), 400
    else:
        return jsonify({"Error": "Invalid team_id or runner_id."}), 400
        
