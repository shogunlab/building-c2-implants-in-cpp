import uuid
import json

from flask import request, Response
from flask_restful import Resource
from database.db import initialize_db
from database.models import Task


class Tasks(Resource):
    # ListTasks
    def get(self):
        # Add behavior for GET here
        return "GET success!", 200

    # AddTasks
    def post(self):
        # Add behavior for POST here
        return "POST success!", 200
