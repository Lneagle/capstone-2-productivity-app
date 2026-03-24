from flask import request, jsonify, make_response
from flask_restful import Resource
from sqlalchemy import desc
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
			return [UserSchema().dump(user) for user in users], 200
		else:
			return {'errors': ['404 Not Found']}, 404
		
class UserById(Resource):
	def get(self, team_id, user_id):
		(user, err_response) = verify_ids(model=User, isList=False, item_id=user_id, team_id=team_id)

		if user:
			return UserSchema().dump(user), 200
		else:
			return err_response

class ClientIndex(Resource):
	def get(self):
		clients = Client.query.all()
    
		if clients:
			return [ClientSchema().dump(client) for client in clients], 200
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
			if not request_json:
				return {'errors': ['Request body required']}, 400
			
			for attr in request_json:
				setattr(client, attr, request_json[attr])
			db.session.commit()
			return ClientSchema().dump(client), 200
		else:
			return {'errors': ['404 Not Found']}, 404
		
class ProjectsByTeam(Resource):
	def get(self, team_id):
		projects = Project.query.filter_by(team_id=team_id).all()

		if projects:
			return [ProjectSchema(exclude=('team',)).dump(project) for project in projects], 200
		else:
			return {'errors': ['404 Not Found']}, 404
		
	def post(self, team_id):
		request_json = request.get_json()
		if not request_json:
			return {'errors': ['Request body required']}, 400
		
		if 'name' not in request_json:
			return {'errors': ['name is required']}, 400
		
		if not isinstance(request_json['name'], str) or not request_json['name'].strip():
			return {'errors': ['name must be a non-empty string']}, 400

		team = Team.query.filter_by(id=team_id).first()
		if not team:
			return {'errors': ['Team not found']}, 404
		
		client = Client.query.filter_by(id=request_json["client_id"]).first()
		if not client:
			return {'errors': ['Client not found']}, 404

		try:
			new_project = Project(name=request_json['name'], completed=False)
			new_project.team = team
			new_project.client = client
			db.session.add(new_project)
			db.session.commit()
			return ProjectSchema().dump(new_project), 201
		except IntegrityError as e:
			db.session.rollback()
			return {'errors': ['Database constraint violation']}, 422
		
class ProjectById(Resource):
	def get(self, team_id, project_id):
		(project, err_response) = verify_ids(model=Project, isList=False, item_id=project_id, team_id=team_id)
		
		if project:
			return ProjectSchema(exclude=('team',)).dump(project), 200
		else:
			return err_response
		
	def patch(self, team_id, project_id):
		(project, err_response) = verify_ids(model=Project, isList=False, item_id=project_id, team_id=team_id)

		if project:
			request_json = request.get_json()
			if not request_json:
				return {'errors': ['Request body required']}, 400

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
				return {'errors': ['405 Method Not Allowed']}, 405 # Do not delete projects that have time entries attached
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
			return [TaskSchema().dump(task) for task in tasks], 200
		else:
			return {'errors': ['404 Not Found']}, 404
		
class TasksByTeam(Resource):
	def get(self, team_id):
		#user = User.query.filter_by(id=user_id).first()

		#if user.admin and user.team_id == team_id:
			tasks = Task.query.join(Project).filter(Project.team_id == team_id).all()
			if tasks:
				return [TaskSchema().dump(task) for task in tasks], 200
			else:
				return {'errors': ['404 Not Found']}, 404
		#else:
			#return {'errors': ['403 Forbidden']}, 403

class TasksByProject(Resource):
	def post(self, team_id, project_id):
		project = Project.query.filter_by(id=project_id).first()

		if project and project.team_id == team_id:
			request_json = request.get_json()
			if not request_json:
				return {'errors': ['Request body required']}, 400
			
			if 'name' not in request_json or 'priority' not in request_json:
				return {'errors': ['name and priority are required']}, 400
			
			if not isinstance(request_json['name'], str) or not request_json['name'].strip():
				return {'errors': ['name must be a non-empty string']}, 400
			
			if request_json['priority'] not in ['High', 'Medium', 'Low']:
				return {'errors': ['priority must be High, Medium, or Low']}, 400
			
			assignee_id = request_json['assignee_id']
			if assignee_id:
				assignee = User.query.filter_by(id=assignee_id).first()
				if not assignee:
					return {'errors': ['Assignee not found']}, 404
		
			try:
				new_task = Task(name=request_json['name'], completed=False, priority=request_json['priority'])
				new_task.project = project
				if assignee_id:
					new_task.assignee = assignee
				db.session.add(new_task)
				db.session.commit()
				return TaskSchema().dump(new_task), 201
			except IntegrityError as e:
				db.session.rollback()
				return {'errors': ['Database constraint violation']}, 422
		else:
			return {'errors': ['403 Forbidden']}, 403

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
			if not request_json:
				return {'errors': ['Request body required']}, 400
			
			for attr in request_json:
				if attr == "assignee_id":
					assignee_id = request_json[attr]
					assignee = User.query.filter_by(id=assignee_id).first()
					if assignee:
						task.assignee = assignee
					else:
						return {'errors': ['Assignee not found']}, 404
				else:
					setattr(task, attr, request_json[attr])
			db.session.commit()
			return TaskSchema().dump(task), 200
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
		if not request.args.get('open_check'):
			start_date = date.today() - timedelta(days=6) # return time entries for the last week
			start_date = datetime.combine(start_date, time(0, 0))
			entries = TimeEntry.query.filter_by(user_id=user_id).filter(TimeEntry.start_time >= start_date).all() 

			if entries:
				if not User.query.filter_by(id=user_id, team_id=team_id).first():
					return {'errors': ['403 Forbidden']}, 403
				return [TimeEntrySchema(exclude=('user',)).dump(entry) for entry in entries], 200
			else:
				return {'errors': ['404 Not Found']}, 404
		else:
			open_entry = TimeEntry.query.filter_by(end_time=None).order_by(desc(TimeEntry.id)).first()
			# return TimeEntrySchema(exclude=('user',)).dump(open_entry), 200
			if open_entry:
				if not user_id == open_entry.user_id:
					return {'errors': ['403 Forbidden']}, 403
				return {'task_id': open_entry.task_id, 'entry_id': open_entry.id}, 200
			else:
				return {'errors': ['404 Not Found']}, 404
		
	def post(self, team_id, user_id):
		request_json = request.get_json()
		if not request_json:
			return {'errors': ['Request body required']}, 400
		
		if 'task_id' not in request_json or 'start_time' not in request_json:
			return {'errors': ['task_id and start_time are required']}, 400

		if not User.query.filter_by(id=user_id, team_id=team_id).first() or not Task.query.filter_by(id=request_json['task_id'], assignee_id=user_id):
			return {'errors': ['403 Forbidden']}, 403
		
		try:
			new_entry = TimeEntry(start_time=datetime.fromtimestamp(request_json['start_time'] / 1000))
			new_entry.user = User.query.filter_by(id=user_id).first()
			new_entry.task = Task.query.filter_by(id=request_json['task_id']).first()
			db.session.add(new_entry)
			db.session.commit()
			return TimeEntrySchema().dump(new_entry), 201
		except IntegrityError as e:
			db.session.rollback()
			return {'errors': ['Database constraint violation']}, 422
		
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
			if not request_json:
				return {'errors': ['Request body required']}, 400
			
			for attr in request_json:
				if attr == "end_time":
					end_time = datetime.fromtimestamp(request_json[attr] / 1000)
					if end_time < entry.start_time:
						return {'errors': ['End time cannot be before start time']}, 400
					setattr(entry, attr, end_time)
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