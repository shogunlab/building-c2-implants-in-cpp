from database.db import db

# Define Task object in database
class Task(db.DynamicDocument):
    task_id = db.StringField(required=True)

# Define Result object in database
class Result(db.DynamicDocument):
    result_id = db.StringField(required=True)
