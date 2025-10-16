#!/usr/bin/env python3

from flask import request, jsonify, make_response
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from config import app, db, api
from models import *

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

api.add_resource(ClientIndex, '/clients', endpoint='clients')
api.add_resource(ClientById, '/clients/<int:id>', endpoint='clients/<int:id>')

if __name__ == '__main__':
  app.run(port=5555, debug=True)