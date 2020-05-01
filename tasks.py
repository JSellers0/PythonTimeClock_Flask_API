"""
This is the task module and supports all REST actions for the task table
"""
from flask import abort
from models import Task, TaskSchema
from config import db

def read_all():
    tasks = Task.query.order_by(Task.task_name).all()

    task_schema = TaskSchema(many=True)
    data = task_schema.dump(tasks)
    return data

# ToDo: Add read_user: Task.join(user_task_exclude).all()

def read_one(taskid):
    task = Task.query.filter(Task.taskid == taskid).one_or_none()

    if task is not None:
        task_schema = TaskSchema()
        data = task_schema.dump(task)
    else:
        abort(
            404,
            "Task Record not found for {}".format(taskid)
        )

def create(task_name):
    existing_task = Task.query.filter(Task.task_name == task_name).one_or_none()

    if existing_task is None:
        schema = TaskSchema()
        new_task = schema.load(task, session=db.session)

        db.session.add(new_task)
        db.session.commit()

        data = schema.dump(new_task)

        return data, 201

    else:
        abort(
            409,
            "Task {} already exists.".format(task_name)
        )

