from flask import request, jsonify, make_response
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from datetime import datetime, date, time, timedelta
from config import db
from models import *

def verify_ids(model, isList, item_id, team_id=None):
	if isList:
		item = model.query.filter_by(id=item_id).all()
	else:
		item = model.query.filter_by(id=item_id).first()
		
	if item:
		if team_id:
			if team_id != item.team_id:
				return (None, make_response({'errors': ['403 Forbidden']}, 403)) # item does not belong to team
		return (item, None)
	else:
		return (None, make_response({'errors': ['404 Not Found']}, 404))

class UsersByTeam(Resource):
	def get(self, team_id):
		users = User.query.filter_by(team_id=team_id).all()

		if users:
			return [UserSchema().dump(user) for user in users]
		else:
			return {'errors': ['404 Not Found']}, 404
		
class UserById(Resource):
	def get(self, team_id, user_id):
		(user, err_response) = verify_ids(model=User, isList=False, item_id=user_id, team_id=team_id)

		if user:
			return UserSchema().dump(user)
		else:
			return err_response

class ClientIndex(Resource):
	def get(self):
		clients = Client.query.all()
    
		if clients:
			return [ClientSchema().dump(client) for client in clients]
		else:
			return {'errors': ['404 Not Found']}, 404
		
class ClientById(Resource):
	def get(self, id):
		client = Client.query.filter_by(id=id).first()

		if client:
			return ClientSchema().dump(client)
		else:
			return {'errors': ['404 Not Found']}, 404
		
	def patch(self, id):
		client = Client.query.filter_by(id=id).first()

		if client:
			request_json = request.get_json()
			for attr in request_json:
				setattr(client, attr, request_json[attr])
			db.session.commit()
			return ClientSchema().dump(client), 200
		else:
			return {'errors': ['404 Not Found']}, 404
		
class ProjectsByTeam(Resource):
	def get(self, team_id):
		projects = Project.query.filter_by(team_id=team_id).all()

		if len(projects) > 0:
			return [ProjectSchema(exclude=('team',)).dump(project) for project in projects]
		else:
			return {'errors': ['404 Not Found']}, 404
		
	def post(self, team_id):
		request_json = request.get_json()
		new_project = Project(name=request_json['name'], completed=False)
		new_project.client = Client.query.filter_by(id=request_json["client_id"]).first()
		new_project.team = Team.query.filter_by(id=team_id).first()
		
		try:
			db.session.add(new_project)
			db.session.commit()
			return ProjectSchema().dump(new_project), 201
		except IntegrityError:
			return {'errors': ['422 Unprocessable Entity']}, 422
		
class ProjectById(Resource):
	def get(self, team_id, project_id):
		(project, err_response) = verify_ids(model=Project, isList=False, item_id=project_id, team_id=team_id)
		
		if project:
			return ProjectSchema(exclude=('team',)).dump(project)
		else:
			return err_response
		
	def patch(self, team_id, project_id):
		(project, err_response) = verify_ids(model=Project, isList=False, item_id=project_id, team_id=team_id)

		if project:
			request_json = request.get_json()
			for attr in request_json:
				setattr(project, attr, request_json[attr])
			db.session.commit()
			return ProjectSchema(exclude=('team',)).dump(project), 200
		else:
			return err_response
		
	def delete(self, team_id, project_id):
		(project, err_response) = verify_ids(model=Project, isList=False, item_id=project_id, team_id=team_id)

		if project:
			time_entries = TimeEntry.query.join(Task).filter(Task.project_id == project_id).all()
			if time_entries:
				return {'errors': ['405 Method Not Allowed']}, 405
			else:
				db.session.delete(project)
				db.session.commit()
				return {}, 204
		else:
			return err_response
		
class TasksByUser(Resource):
	def get(self, team_id, user_id):
		tasks = Task.query.filter_by(assignee_id=user_id).all()

		if tasks:
			if not User.query.filter_by(id=user_id, team_id=team_id).first():
				return {'errors': ['403 Forbidden']}, 403
			return [TaskSchema().dump(task) for task in tasks]
		else:
			return {'errors': ['404 Not Found']}, 404
		
# TODO: Create TaskById (under projects: get, patch, delete), TasksByProject (get, post)

class TasksByProject(Resource):
	def post(self, client_id, project_id):
		pass

class TaskById(Resource):
	def get(self, client_id, project_id, task_id):
		task = Task.query.filter_by(id=task_id).first()

		if task:
			if task.project_id != project_id or task.project.client_id != client_id:
				return {'errors': ['403 Forbidden']}, 403
			return TaskSchema().dump(task)
		else:
			return {'errors': ['404 Not Found']}, 404
		
	def patch(self, client_id, project_id, task_id):
		task = Task.query.filter_by(id=task_id).first()

		if task:
			if task.project_id != project_id or task.project.client_id != client_id:
				return {'errors': ['403 Forbidden']}, 403
			request_json = request.get_json()
			for attr in request_json:
				setattr(task, attr, request_json[attr])
			db.session.commit()
			return TaskSchema(exclude=('project',)).dump(task), 200
		else:
			return {'errors': ['404 Not Found']}, 404
		
	def delete(self, client_id, project_id, task_id):
		task = Task.query.filter_by(id=task_id).first()

		if task:
			if task.project_id != project_id or task.project.client_id != client_id:
				return {'errors': ['403 Forbidden']}, 403
			if not task.time_entries:
				db.session.delete(task)
				db.session.commit()
				return {}, 204
			else:
				return {'errors': ['403 Forbidden']}, 403
		else:
			return {'errors': ['404 Not Found']}, 404
		
class TimeEntriesByUser(Resource):
	def get(self, team_id, user_id):
		start_date = date.today() - timedelta(days=6) # return time entries for the last week
		start_date = datetime.combine(start_date, time(0, 0))
		entries = TimeEntry.query.filter_by(user_id=user_id).filter(TimeEntry.start_time >= start_date).all() 

		if entries:
			if not User.query.filter_by(id=user_id, team_id=team_id).first():
				return {'errors': ['403 Forbidden']}, 403
			return [TimeEntrySchema(exclude=('user',)).dump(entry) for entry in entries]
		else:
			return {'errors': ['404 Not Found']}, 404
		
	def post(self, team_id, user_id):
		request_json = request.get_json()

		if not User.query.filter_by(id=user_id, team_id=team_id).first() or not Task.query.filter_by(id=request_json['task_id'], assignee_id=user_id):
				return {'errors': ['403 Forbidden']}, 403
		new_entry = TimeEntry(start_time=datetime.fromtimestamp(request_json['start_time'] / 1000))
		new_entry.user = User.query.filter_by(id=user_id).first()
		new_entry.task = Task.query.filter_by(id=request_json['task_id']).first()
		
		try:
			db.session.add(new_entry)
			db.session.commit()
			return TimeEntrySchema().dump(new_entry), 201
		except IntegrityError:
			return {'errors': ['422 Unprocessable Entity']}, 422
		
class TimeEntryById(Resource):
	def get(self, team_id, user_id, entry_id):
		entry = TimeEntry.query.filter_by(id=entry_id).first()

		if entry:
			if not User.query.filter_by(id=user_id, team_id=team_id).first() or not entry.user_id == user_id:
				return {'errors': ['403 Forbidden']}, 403
			return TimeEntrySchema().dump(entry), 200
		else:
			return {'errors': ['404 Not Found']}, 404

	def patch(self, team_id, user_id, entry_id):
		entry = TimeEntry.query.filter_by(id=entry_id).first()

		if entry:
			if not entry.user_id == user_id:
				return {'errors': ['403 Forbidden']}, 403
			request_json = request.get_json()
			for attr in request_json:
				if attr == "end_time":
					setattr(entry, attr, datetime.fromtimestamp(request_json[attr] / 1000))
				else:
					setattr(entry, attr, request_json[attr])
			db.session.commit()
			return TimeEntrySchema().dump(entry), 200
		else:
			return {'errors': ['404 Not Found']}, 404
		
	def delete(self, team_id, user_id, entry_id):
		entry = TimeEntry.query.filter_by(id=entry_id).first()

		if entry:
			if not User.query.filter_by(id=user_id, team_id=team_id).first():
				return {'errors': ['403 Forbidden']}, 403
			db.session.delete(entry)
			db.session.commit()
			return {}, 204
		else:
			return {'errors': ['404 Not Found']}, 404