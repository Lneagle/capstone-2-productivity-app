#!/usr/bin/env python3

from sqlalchemy import text
from random import choice as rc
from faker import Faker
from config import db, app
from models import *

fake = Faker()

with app.app_context():
  print('Deleting all records...')
  # User.query.delete()
  # Team.query.delete()
  db.session.execute(text('TRUNCATE TABLE teams RESTART IDENTITY CASCADE; TRUNCATE TABLE clients RESTART IDENTITY CASCADE;')) # deletes all data and resets ids

  print('Creating teams...')
  team1 = Team(name="Dev", department="Operations")
  team2 = Team(name="Payroll", department="HR")

  db.session.add_all([team1, team2])
  
  print('Creating users...')
  team1_admin = User(name="Dev Admin", admin=True)
  team1_admin.team = team1
  team2_admin = User(name="Payroll Admin", admin=True)
  team2_admin.team = team2

  users = []
  usernames = []

  for i in range(10):
    username = fake.first_name()
    while username in usernames: # Guarantee uniqueness
      username = fake.first_name()
    usernames.append(username)
    user = User(name=username, admin=False)
    user.team = rc([team1, team2])
    users.append(user)

  db.session.add_all([team1_admin, team2_admin, *users])

  print('Creating clients...')
  client1 = Client(name='Viridian Dynamics', contact="Veronica")
  client2 = Client(name='Dunder Mifflin', contact="Michael")
  client3 = Client(name='Kwik-E-Mart', contact="Apu")

  db.session.add_all([client1, client2, client3])

  print('Creating projects...')
  projects = []

  for i in range(10):
    project = Project(name=fake.catch_phrase(), completed=False)
    project.client = rc([client1, client2, client3])
    projects.append(project)

  db.session.add_all(projects)

  print('Creating tasks...')
  tasks = []

  for i in range(50):
    task = Task(name=fake.bs(), completed=False, priority=rc(['High', 'Medium', 'Low']))
    task.project = rc(projects)
    tasks.append(task)

  db.session.add_all(projects)

  db.session.commit()
  print('Complete')
  db.session.close()