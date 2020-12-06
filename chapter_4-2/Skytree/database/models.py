from database.db import db

# Define Task object in database
class Task(db.DynamicDocument):
    task_id = db.StringField(required=True)

# Define Result object in database
class Result(db.DynamicDocument):
    result_id = db.StringField(required=True)

# Define TaskHistory object in database
class TaskHistory(db.DynamicDocument):
    task_object = db.StringField()
