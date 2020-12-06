from database.db import db

# Define Task object in database
class Task(db.DynamicDocument):
    task_id = db.StringField(required=True)
