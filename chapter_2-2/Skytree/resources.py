import uuid
import json

from flask import request, Response
from flask_restful import Resource
from database.db import initialize_db
from database.models import Task


class Tasks(Resource):
    # ListTasks
    def get(self):
        # Get all the task objects and return them to the user
        tasks = Task.objects().to_json()
        return Response(tasks, mimetype="application/json", status=200)

    # AddTasks
    def post(self):
        # Parse out the JSON body we want to add to the database
        body = request.get_json()
        json_obj = json.loads(json.dumps(body))
        # Get the number of Task objects in the request
        obj_num = len(body)
        # For each Task object, add it to the database
        for i in range(len(body)):
            # Add a task UUID to each task object for tracking
            json_obj[i]['task_id'] = str(uuid.uuid4())
            # Save Task object to database
            Task(**json_obj[i]).save()
            # Load the options provided for the task into an array for tracking in history
            task_options = []
            for key in json_obj[i].keys():
                # Anything that comes after task_type and task_id is treated as an option
                if (key != "task_type" and key != "task_id"):
                    task_options.append(key + ": " + json_obj[i][key])
        # Return the last Task objects that were added
        return Response(Task.objects.skip(Task.objects.count() - obj_num).to_json(),
                        mimetype="application/json",
                        status=200)
