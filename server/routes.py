from flask import request, jsonify, make_response
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
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