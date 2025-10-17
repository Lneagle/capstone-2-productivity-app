#!/usr/bin/env python3

from flask import request, jsonify, make_response
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from config import app, db, api
from models import *

class UsersByTeam(Resource):
	def get(self, team_id):
		users = User.query.filter_by(team_id=team_id).all()

		if len(users) > 0:
			return [UserSchema().dump(user) for user in users]
		else:
			return {'errors': ['404 Not Found']}, 404

class ClientIndex(Resource):
	def get(self):
		clients = Client.query.all()
    
		if len(clients) > 0:
			return [ClientSchema().dump(client) for client in clients]
		else:
			return {'errors': ['404 Not Found']}, 404
		
	def post(self):
		request_json = request.get_json()
		new_client = Client(name=request_json['name'], contact=request_json.get('contact'))
		
		try:
			db.session.add(new_client)
			db.session.commit()
			return ClientSchema().dump(new_client), 201
		except IntegrityError:
			return {'errors': ['422 Unprocessable Entity']}, 422
		
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
		project = Project.query.filter_by(id=project_id).first()

		if project:
			if project.team_id == team_id:
				return ProjectSchema(exclude=('team',)).dump(project)
			else:
				return {'errors': ['403 Forbidden']}, 403 #project does not belong to team
		else:
			return {'errors': ['404 Not Found']}, 404
		
	def patch(self, team_id, project_id):
		project = Project.query.filter_by(id=project_id).first()

		if project:
			if project.team_id == team_id:
				request_json = request.get_json()
				for attr in request_json:
					setattr(project, attr, request_json[attr])
				db.session.commit()
				return ProjectSchema(exclude=('team',)).dump(project), 200
			else:
				return {'errors': ['403 Forbidden']}, 403 #project does not belong to team
		else:
			return {'errors': ['404 Not Found']}, 404

		

api.add_resource(UsersByTeam, '/teams/<int:team_id>/users', endpoint='/teams/<int:team_id>/users')
api.add_resource(ClientIndex, '/clients', endpoint='clients')
api.add_resource(ClientById, '/clients/<int:id>', endpoint='clients/<int:id>')
api.add_resource(ProjectsByTeam, '/teams/<int:team_id>/projects', endpoint='/teams/<int:team_id>/projects')
api.add_resource(ProjectById, '/teams/<int:team_id>/projects/<int:project_id>', endpoint='/teams/<int:team_id>/projects/<int:project_id>')

if __name__ == '__main__':
  app.run(port=5555, debug=True)