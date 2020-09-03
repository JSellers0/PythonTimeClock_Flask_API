"""
This is the Project module and supports all REST actions for the project table
"""
from flask import abort
from models import Project, ProjectSchema
from config import db

def read_all():
    projects = Project.query.order_by(Project.project_name).all()

    project_schema = ProjectSchema(many=True)
    data = project_schema.dump(projects)
    return data

# ToDo: Add read_user_all: Project.join(user_project_exclude).all()

def read_one(projectid):
    project = Project.query.filter(Project.projectid == projectid).one_or_none()

    if project is not None:
        project_schema = ProjectSchema()
        data = project_schema.dump(project)
        return data, 200
    else:
        abort(
            404,
            "Project Record not found for {}".format(projectid)
        )

def create(project_name):
    existing_project = Project.query.filter(Project.project_name == project_name).one_or_none()

    if existing_project is None:
        new_project = Project(project_name)

        db.session.add(new_project)
        db.session.commit()

        schema = ProjectSchema()
        data = schema.dump(new_project)

        return data, 201

    else:
        abort(
            409,
            "Project {} already exists.".format(project_name)
        )

def update(projectid, project_name):
    update_project = Project.query.filter(Project.projectid == projectid).one_or_none()

    existing_project = Project.query.filter(Project.project_name == project_name).one_or_none()

    if update_project is None:
        abort(
            404, 
            "Project not found for ID {}.".format(projectid)
        )
    elif existing_project is not None:
        abort(
            409,
            "Project {} already exists.".format(project_name)
        )
    else:
        update = Project(project_name)
        update.projectid = projectid

        db.session.merge(update)
        db.session.commit()

        schema = ProjectSchema()
        data = schema.dump(update)

        return data, 200

