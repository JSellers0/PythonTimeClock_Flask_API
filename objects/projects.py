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
        schema = ProjectSchema()
        new_project = schema.load({"project_name": project_name}, session=db.session)

        db.session.add(new_project)
        db.session.commit()

        data = schema.dump(new_project)

        return data, 201

    else:
        abort(
            409,
            "Project {} already exists.".format(project_name)
        )

def update(projectid, project):
    update_project = Project.query.filter(Project.projectid == projectid).one_or_none()

    new_project_name = project.get("project_name")
    existing_project = Project.query.filter(Project.project_name == new_project_name).one_or_none()

    if update_project is None:
        abort(
            404, 
            "Project not found for ID {}.".format(projectid)
        )
    elif existing_project is not None:
        abort(
            409,
            "Project {} already exists.".format(new_project_name)
        )
    else:
        schema = ProjectSchema()
        update = schema.load(project, session=db.session)

        db.session.merge(update)
        db.session.commit()

        data = schema.dump(project)

        return data, 200

