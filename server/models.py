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
  tasks = db.relationship('Task', back_populates='assignee')

  time_entries = db.relationship('TimeEntry', back_populates='user')

  def __repr__(self):
    return f'<User {self.name} {self.team.name}>'

class Client(db.Model):
  __tablename__ = 'clients'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, unique=True, nullable=False)
  contact = db.Column(db.String)

  projects = db.relationship('Project', back_populates='client')

  def __repr__(self):
    return f'<Client {self.name}>'
  
class Project(db.Model):
  __tablename__ = 'projects'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  completed = db.Column(db.Boolean)

  client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))

  client = db.relationship('Client', back_populates='projects')
  tasks = db.relationship('Task', back_populates='project')

  def __repr__(self):
    return f'<Project {self.name}>'
  
class Task(db.Model):
  __tablename__ = 'tasks'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  completed = db.Column(db.Boolean)
  priority = db.Column(db.String)

  project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
  assignee_id = db.Column(db.Integer, db.ForeignKey('users.id'))

  project = db.relationship('Project', back_populates='tasks')
  assignee = db.relationship('User', back_populates='tasks')

  time_entries = db.relationship('TimeEntry', back_populates='task')

  def __repr__(self):
    return f'<Task {self.name}>'
  
class TimeEntry(db.Model):
  __tablename__ = 'time_entries'

  id = db.Column(db.Integer, primary_key=True)
  start_time = db.Column(db.DateTime, nullable=False)
  end_time = db.Column(db.DateTime)

  task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'))
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

  task = db.relationship('Task', back_populates='time_entries')
  user = db.relationship('User', back_populates='time_entries')

  def __repr__(self):
    return f'<TimeEntry {self.start_time} - {self.end_time}>'