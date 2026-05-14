#!/usr/bin/env python3

from sqlalchemy import text
from random import choice as rc, randrange
from faker import Faker
from datetime import timedelta
from config import db, app
from models import *

fake = Faker()

with app.app_context():
  
	tasks = db.session.query(Task).all()

	print('Creating time entries...')

	entries = []

	for i in range(100):
		start = fake.past_datetime('-7d')
		while start.weekday() > 4 or start.time().hour < 8 or start.time().hour > 17:
			start = fake.past_datetime('-7d')
		interval = randrange(15, 120)
		end = start + timedelta(minutes=interval)
		entry = TimeEntry(start_time=start, end_time=end)
		entry.task = rc(tasks)
		entry.user = entry.task.assignee
		entries.append(entry)

	db.session.add_all(entries)

	db.session.commit()
	print('Complete')
	db.session.close()