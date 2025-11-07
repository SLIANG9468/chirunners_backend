from app.extensions import ma
from app.models import Team, Team_Runner_Role
from marshmallow import fields

class TeamSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Team
        include_fk = True

team_schema = TeamSchema()
teams_schema = TeamSchema(many=True) #handle a list of teams

class TeamRunnerRoleSchema(ma.SQLAlchemyAutoSchema):
    runner = fields.Nested("RunnerSchema")
    class Meta:
        model = Team_Runner_Role
        include_fk = True
        fields = ("runner", "role")

team_runner_role_schema = TeamRunnerRoleSchema()
team_runner_roles_schema = TeamRunnerRoleSchema(many=True) #handle a list of team_runner_roles
