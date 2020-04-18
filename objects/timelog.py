"""
This is the Timelog module and supports all REST actions for the timelog table
"""
from flask import abort
from api.models import Timelog, TimelogSchema
from api.config import db

def read_all():
    timelogs = Timelog.query.order_by(Timelog.timelog_name).all()

    timelog_schema = TimelogSchema(many=True)
    data = timelog_schema.dump(timelogs)
    return data

def read_one(timelogid):
    timelog = Timelog.query.filter(Timelog.timelogid == timelogid).one_or_none()

    if timelog is not None:
        timelog_schema = TimelogSchema()
        data = timelog_schema.dump(timelog)
    else:
        abort(
            404,
            "Timelog Record not found for {}".format(timelogid)
        )

def create(timelog):
    existing_timelog = Timelog.query.filter(Timelog.timelogid == timelogid.get("timelogid")).one_or_none()

    if existing_timelog is None:
        schema = TimelogSchema()
        new_timelog = schema.load(timelog, session=db.session)

        db.session.add(new_timelog)
        db.session.commit()

        data = schema.dump(new_timelog)

        return data, 201

    else:
        abort(
            409,
            "Timelog {} already exists.".format(timelog.get("timelogid"))
        )

def update(timelogid, timelog):
    update_timelog = Timelog.query.filter(Timelog.timelogid == timelogid).one_or_none()

    if update_timelog is None:
        abort(
            404,
            "Timelog Row not found for ID: {}".format(timelogid)
        )
    else:
        schema = TimelogSchema()
        update = schema.load(timelog, session=db.session)

        db.session.merge(update)
        db.session.commit()

        data = schema.dump(update_timelog)

        return data, 200

