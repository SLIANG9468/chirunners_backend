from app.extensions import ma
from app.models import Runner

class RunnerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Runner
        include_fk = True


runner_schema = RunnerSchema()
runners_schema = RunnerSchema(many=True) #handle a list of runners
login_schema = RunnerSchema(only=["email", "password"])