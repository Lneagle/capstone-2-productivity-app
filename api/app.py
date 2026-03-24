#!/usr/bin/env python3

from config import app, db, api
from routes import *

api.add_resource(UsersByTeam, '/teams/<int:team_id>/users', endpoint='/teams/<int:team_id>/users')
api.add_resource(UserById, '/teams/<int:team_id>/users/<int:user_id>', endpoint='/teams/<int:team_id>/users/<int:user_id>')
api.add_resource(ClientIndex, '/clients', endpoint='clients')
api.add_resource(ClientById, '/clients/<int:id>', endpoint='clients/<int:id>')
api.add_resource(ProjectsByTeam, '/teams/<int:team_id>/projects', endpoint='/teams/<int:team_id>/projects')
api.add_resource(ProjectById, '/teams/<int:team_id>/projects/<int:project_id>', endpoint='/teams/<int:team_id>/projects/<int:project_id>')
api.add_resource(TasksByUser, '/teams/<int:team_id>/users/<int:user_id>/tasks', endpoint='/teams/<int:team_id>/users/<int:user_id>/tasks')
api.add_resource(TasksByTeam, '/teams/<int:team_id>/projects/tasks', endpoint='/teams/<int:team_id>/projects/tasks')
api.add_resource(TasksByProject, '/teams/<int:team_id>/projects/<int:project_id>/tasks', endpoint='/teams/<int:team_id>/projects/<int:project_id>/tasks')
api.add_resource(TaskById, '/clients/<int:client_id>/projects/<int:project_id>/tasks/<int:task_id>', endpoint='/clients/<int:client_id>/projects/<int:project_id>/tasks/<int:task_id>')
api.add_resource(TimeEntriesByUser, '/teams/<int:team_id>/users/<int:user_id>/time_entries', endpoint='/teams/<int:team_id>/users/<int:user_id>/time_entries')
api.add_resource(TimeEntryById, '/teams/<int:team_id>/users/<int:user_id>/time_entries/<int:entry_id>', endpoint='/teams/<int:team_id>/users/<int:user_id>/time_entries/<int:entry_id>')

if __name__ == '__main__':
  app.run(port=5555, debug=True)