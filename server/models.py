from sqlalchemy.orm import validates
from marshmallow import Schema, fields

from config import db

class Team(db.Model):
  __tablename__ = 'teams'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  department = db.Column(db.String)

  users = db.relationship('User', back_populates='team')

  def __repr__(self):
    return f'<Team {self.id} {self.name}>'

class User(db.Model):
  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, unique=True, nullable=False)
  admin = db.Column(db.Boolean, nullable=False)

  team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))

  team = db.relationship('Team', back_populates='users')

  def __repr__(self):
    return f'<User {self.name} {self.team.name}>'

