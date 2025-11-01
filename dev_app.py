from app import create_app
from app.models import Team, Runner, db

app = create_app('DevelopmentConfig')

with app.app_context():

    #db.drop_all()

    db.create_all() #Creating our table from our DB models
    # add a initial team "Chi Running CLub"

app.run()