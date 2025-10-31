from app.extensions import ma
from app.models import Team

class TeamSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Team

team_schema = TeamSchema()
teams_schema = TeamSchema(many=True) #handle a list of teams
