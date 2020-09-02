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
        return task.to_json(), 200
    else:
        abort(
            404,
            "Task Record not found for {}".format(taskid)
        )

def create(task_name):
    existing_task = Task.query.filter(Task.task_name == task_name).one_or_none()

    if existing_task is None:
        schema = TaskSchema()
        new_task = schema.load({"task_name": task_name}, session=db.session)

        db.session.add(new_task)
        db.session.commit()

        data = schema.dump(new_task)

        return data, 201

    else:
        abort(
            409,
            "Task {} already exists.".format(task_name)
        )

def update(taskid, task):
    update_task = Task.query.filter(Task.taskid == taskid).one_or_none()

    new_task_name = task.get("task_name")
    existing_task = Task.query.filter(Task.task_name == new_task_name).one_or_none()

    if update_task is None:
        abort(
            404, 
            "Task not found for ID {}.".format(taskid)
        )
    elif existing_task is not None:
        abort(
            409,
            "Task {} already exists.".format(new_task_name)
        )
    else:
        schema = TaskSchema()
        update = schema.load(task, session=db.session)

        db.session.merge(update)
        db.session.commit()

        data = schema.dump(task)

        return data, 200

