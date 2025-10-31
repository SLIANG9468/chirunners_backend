#Where I will initialize SQLAlchemy and create my models
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Date, Integer, DateTime, Table, Column, String, ForeignKey
from datetime import datetime, date

#Create Base Model to be inherited from
class Base(DeclarativeBase):
    pass

#Instatiate db and set Base model
db = SQLAlchemy(model_class=Base)

class Runner(Base):
    __tablename__ = 'runners'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name:Mapped[str] = mapped_column(String(100),nullable = False)
    #For visitors, they may only submit firstname without lastname. Using Frontend to control nullable = False for members
    last_name:Mapped[str] = mapped_column(String(100),nullable = True)
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

class Team(Base):
    __tablename__ = 'teams'

    id: Mapped[int] = mapped_column(primary_key=True)
    team_name:Mapped[str] = mapped_column(String(300),nullable = False)
    country:Mapped[str] = mapped_column(String(300), nullable=False)
    city:Mapped[str] = mapped_column(String(300), nullable=True)
    contact_name:Mapped[str] = mapped_column(String(300),nullable = True)
    contact_email: Mapped[str] = mapped_column(String(360), nullable=False, unique=True)
    regular_group_run:Mapped[str] = mapped_column(Integer)

class Team_Runner_Role(Base):
    __tablename__ = 'team_runner_role'

    id: Mapped[int] = mapped_column(primary_key=True)
    team_id:Mapped[int] = mapped_column(ForeignKey('teams.id'),nullable = False)
    runner_id:Mapped[int] = mapped_column(ForeignKey('runners.id'),nullable = False)
    role:Mapped[str] = mapped_column(String(100), nullable=False)

