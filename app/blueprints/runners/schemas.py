from app.extensions import ma
from app.models import Runner

class RunnerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Runner


runner_schema = RunnerSchema()
runners_schema = RunnerSchema(many=True) #handle a list of runners
