#Where I will initialize SQLAlchemy and create my models
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Date, Integer, DateTime, String, ForeignKey, Table
from datetime import datetime, date

#Create Base Model to be inherited from
class Base(DeclarativeBase):
    pass

#Instatiate db and set Base model
db = SQLAlchemy(model_class=Base)

invites = Table(
    "team_invites",
    Base.metadata,
    db.Column("runner_id", db.ForeignKey("runners.id")),
    db.Column("team_id", db.ForeignKey("teams.id"))
)

class Team(Base):
    __tablename__ = 'teams'

    id: Mapped[int] = mapped_column(primary_key=True)
    team_name:Mapped[str] = mapped_column(String(300),nullable=False, unique=True)
    country:Mapped[str] = mapped_column(String(300), nullable=False)
    city:Mapped[str] = mapped_column(String(300), nullable=True)
    team_contact_id:Mapped[int] = mapped_column(ForeignKey('runners.id'),nullable = False)

    invites: Mapped[list['Runner']] = relationship(secondary="team_invites", back_populates='invites')
    team_runner_roles: Mapped[list['Team_Runner_Role']] = relationship(back_populates='team')
    team_contact: Mapped['Runner'] = relationship(back_populates='created_teams')

class Runner(Base):
    __tablename__ = 'runners'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name:Mapped[str] = mapped_column(String(100),nullable = False)
    #For visitors, they may only submit firstname without lastname. Using Frontend to control nullable = False for members
    last_name:Mapped[str] = mapped_column(String(100), nullable = True)
    email: Mapped[str] = mapped_column(String(360), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(500), nullable=False)
    address_street:Mapped[str] = mapped_column(String(500), nullable=True)
    address_zipcode:Mapped[str] = mapped_column(String(50), nullable=True)
    address_city:Mapped[str] = mapped_column(String(100), nullable=True)
    address_state:Mapped[str] = mapped_column(String(50), nullable=True)
    birth_date:Mapped[date] = mapped_column(Date, nullable=True)
    phone: Mapped[str] = mapped_column(String(50), nullable=True)
    gender: Mapped[str] = mapped_column(String(20), nullable=True)
    wechat_id:Mapped[str] = mapped_column(String(100), nullable=True)
    waivers_sign_timestamp:Mapped[datetime] = mapped_column(DateTime, nullable=True)
    expiration_date: Mapped[date] = mapped_column(Date, nullable=True)

    created_teams: Mapped[list['Team']] = relationship(back_populates='team_contact')
    team_runner_roles: Mapped[list['Team_Runner_Role']] = relationship(back_populates='runner')
    invites: Mapped[list['Team']] = relationship(secondary="team_invites",back_populates='invites')

# Each runner can belong to multiple teams, and each team can include multiple runners.
# A runner can have one specific role (e.g., member, volunteer, admin, board) within each team.
# If a runner holds an admin or board role, they must also be a member and volunteer in that team.
# The combination of (team_id, runner_id) must be unique — one role per runner per team.

class Team_Runner_Role(Base):
    __tablename__ = 'team_runner_roles'

    id: Mapped[int] = mapped_column(primary_key=True)
    team_id:Mapped[int] = mapped_column(ForeignKey('teams.id'),nullable = False)
    runner_id:Mapped[int] = mapped_column(ForeignKey('runners.id'),nullable = False)
    role:Mapped[str] = mapped_column(String(100), nullable=False, default='member')

    runner: Mapped['Runner'] = relationship('Runner', back_populates='team_runner_roles')
    team:Mapped['Team'] = relationship('Team', back_populates='team_runner_roles')

