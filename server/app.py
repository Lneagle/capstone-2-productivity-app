#!/usr/bin/env python3

from config import app, db, api
from routes import *

api.add_resource(UsersByTeam, '/teams/<int:team_id>/users', endpoint='/teams/<int:team_id>/users')
api.add_resource(ClientIndex, '/clients', endpoint='clients')
api.add_resource(ClientById, '/clients/<int:id>', endpoint='clients/<int:id>')
api.add_resource(ProjectsByTeam, '/teams/<int:team_id>/projects', endpoint='/teams/<int:team_id>/projects')
api.add_resource(ProjectById, '/teams/<int:team_id>/projects/<int:project_id>', endpoint='/teams/<int:team_id>/projects/<int:project_id>')

if __name__ == '__main__':
  app.run(port=5555, debug=True)