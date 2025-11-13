from app import create_app
from app.models import Team, Runner, db, Team_Runner_Role
from werkzeug.security import generate_password_hash
from datetime import date

app = create_app('DevelopmentConfig')

with app.app_context():

    db.drop_all()
    db.create_all() #Creating our table from our DB models
    
    # Preload demo data for Sherri
    runner1 = Runner(
        first_name="Sherri",
        last_name="Liang-Zhou",
        email="sherri@chirunners.org",
        password=generate_password_hash("123"),
        address_street="211 Wells St.",
        address_zipcode="60610",
        address_city="Chicago",
        address_state="IL",
        birth_date=date(1980, 1, 1),
        phone="847-111-1111",
        gender="female",
        wechat_id="sherriliangzhou"
    )
    
    db.session.add(runner1)
    db.session.commit()
    
    # Add Chi Running Club team
    team1 = Team(
        team_name="Chi Running Club",
        country="United States",
        city="Chicago",
        team_contact_id=runner1.id
    )
    
    db.session.add(team1)
    db.session.commit()
    
    # Add team_runner_role for Sherri as admin
    team_runner_role1 = Team_Runner_Role(
        team_id=team1.id,
        runner_id=runner1.id,
        role='admin'
    )
    
    db.session.add(team_runner_role1)
    db.session.commit()


app.run()