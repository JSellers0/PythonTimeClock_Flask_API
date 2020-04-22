"""
This is the Timelog module and supports all REST actions for the timelog table
"""
from flask import abort
from api.models import Timelog, TimelogSchema
from api.config import db

def read_user_rows(userid):
    timelogs = Timelog.query.filter(Timelog.userid == userid).order_by(Timelog.timelogid).all()

    timelog_schema = TimelogSchema(many=True)
    data = timelog_schema.dump(timelogs)
    return data, 200

def read_user_current_row(userid):
    timelog = (
        Timelog.query
        .filter(Timelog.userid == userid)
        .order_by(Timelog.timelogid.desc())
        .first()
    )

    if timelog is not None:
        timelog_schema = TimelogSchema()
        data = timelog_schema.dump(timelogs)
        return data, 200
    else:
        abort(
            404,
            "Current Timelog Record not found for {}".format(userid)
        )

def read_user_rows_daterange(userid, daterange):
    range_start = daterange.get("range_start")
    range_end = daterange.get("range_end")

    timelogs = (
        Timelog.query.filter(
            Timelog.userid == userid
        ).filter(
            Timelog.start < range_end
        ).filter(or_(
            Timelog.end > range_start,
            Timelog.end == None
            )
        )
    )

    if timelogs is not None:
        timelog_schema = TimelogSchema(many=True)
        data = timelog_schema.dump(timelogs)
        return data, 200
    else:
        abort(
            404,
            "Timelogs not found for {userid} between {start} and {end}".format(
                userid=userid, start=range_start, end=range_end
            )
        )

def create(userid, timelog_row):
    start = timelog_row.get("start")
    stop = timelog_row.get("stop")
    
    existing_timelog = (
        Timelog.query
        .filter(Timelog.userid == userid)
        .filter(Timelog.start == start)
        .filter(Timelog.stop == stop)
        .one_or_none()
    )

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
            ("Attempting to duplicate Timelog {tlid} start ands top for {userid}."
            .format(tlid=existing_timelog.timelogid, userid=userid)
            )
        )

def update_row(timelogid, timelog):
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

def update_user_current_row(userid, timelog):
    update_timelog = (
        Timelog.query
        .filter(Timelog.userid == userid)
        .order_by(Timelog.timelogid.desc())
        .first()
    )

    if update_timelog is None:
        abort(
            404,
            "Current Timelog Row not found for user {}".format(userid)
        )
    else:
        schema = TimelogSchema()
        update = schema.load(timelog, session=db.session)

        db.session.merge(update)
        db.session.commit()

        data = schema.dump(update_timelog)

        return data, 200

