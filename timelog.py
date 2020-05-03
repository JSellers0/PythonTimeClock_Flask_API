"""
This is the Timelog module and supports all REST actions for the timelog table
"""
import json
from datetime import datetime as dt
from flask import abort
from models import Timelog, TimelogSchema, Project, Task, Note
from config import db
from sqlalchemy import or_

def read_user_rows(userid):
    userid = userid.get("userid")
    timelogs = Timelog.query.filter(Timelog.userid == userid).order_by(Timelog.timelogid).all()

    if len(timelogs ) == 0:
        abort(
            404,
            "No Timelog rows found for User {}".format(userid)
        )
    else:
        timelog_schema = TimelogSchema(many=True)
        data = timelog_schema.dump(timelogs)
        return data, 200

def create(timelog):
    userid = timelog.get("userid")
    start = dt.strptime(timelog.get("start"), "%Y-%m-%dT%H:%M:%SZ")
    stop = timelog.get("stop")

    if stop == "na":
        existing_timelog = (
            Timelog.query
            .filter(Timelog.userid == userid)
            .filter(Timelog.start == start)
            .one_or_none()
        )
    else:
        stop = dt.strptime(timelog.get("stop"), "%Y-%m-%dT%H:%M:%SZ")
        existing_timelog = (
            Timelog.query
            .filter(Timelog.userid == userid)
            .filter(Timelog.start == start)
            .filter(Timelog.stop == stop)
            .one_or_none()
        )
        
    if existing_timelog is None:
        if stop == "na":
            new_timelog = Timelog(
                userid=timelog.get("userid"),
                projectid=timelog.get("projectid"),
                taskid=timelog.get("taskid"),
                noteid=timelog.get("noteid"),
                start=start
            )
        else:
            new_timelog = Timelog(
                userid=timelog.get("userid"),
                projectid=timelog.get("projectid"),
                taskid=timelog.get("taskid"),
                noteid=timelog.get("noteid"),
                start=start,
                stop=stop
            )

        db.session.add(new_timelog)
        db.session.commit()

        return new_timelog.to_json(), 201

    else:
        abort(
            409,
            ("Attempting to duplicate Timelog {tlid} start and stop for {userid}."
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
        schema = TimelogSchema(partial=("userid", "projectid", "taskid", "noteid", ))
        update = schema.load(timelog, session=db.session)

        db.session.merge(update)
        db.session.commit()

        return 201

def read_row_detail(timelogid):
    timelog = Timelog.query.filter(Timelog.timelogid == timelogid).one_or_none()
    
    if timelog is None:
        abort(
            404,
            "No row found for {}".format(timelogid)
        )
    else:
        task = Task.query.filter(Task.taskid == timelog.taskid).one_or_none()
        project = Project.query.filter(Project.projectid == timelog.projectid).one_or_none()
        note = Note.query.filter(Note.noteid == timelog.noteid).one_or_none()
        timelog_dump = {
            "timelogid": str(timelog.timelogid),
            "userid": str(timelog.userid),
            "taskid": str(timelog.taskid),
            "task_name": task.task_name,
            "projectid": str(timelog.projectid),
            "project_name": project.project_name,
            "noteid": str(note.noteid),
            "note_name": note.note_name,
            "start": timelog.start.strftime("%Y-%m-%d %H:%M:%S"),
            "stop": timelog.stop.strftime("%Y-%m-%d %H:%M:%S")
        }
        return json.dumps(timelog_dump), 200

def read_daterange(userid, range_begin, range_end):
    range_start = dt.strptime(range_begin, "\"%Y-%m-%d %H:%M:%S\"")
    range_end = dt.strptime(range_end, "\"%Y-%m-%d %H:%M:%S\"")

    timelogs = (
        Timelog.query.filter(
            Timelog.userid == userid
        ).filter(
            Timelog.start < range_end
        ).filter(or_(
            Timelog.stop > range_start,
            Timelog.stop == None
            )
        )
    )

    if [timelog for timelog in timelogs]:
        timelog_dump = {"rows": []}
        for timelog in timelogs:
            task = Task.query.filter(Task.taskid == timelog.taskid).one_or_none()
            project = Project.query.filter(Project.projectid == timelog.projectid).one_or_none()
            note = Note.query.filter(Note.noteid == timelog.noteid).one_or_none()
            timelog_row = {
                "timelogid": str(timelog.timelogid),
                "userid": str(timelog.userid),
                "taskid": str(timelog.taskid),
                "task_name": task.task_name,
                "projectid": str(timelog.projectid),
                "project_name": project.project_name,
                "noteid": str(note.noteid),
                "note_name": note.note_name,
                "start": timelog.start.strftime("%Y-%m-%d %H:%M:%S"),
                "stop": timelog.stop.strftime("%Y-%m-%d %H:%M:%S")
            }
            timelog_dump["rows"].append(timelog_row)

            print(timelog_dump)

        return json.dumps(timelog_dump), 200

    else:
        abort(
            404,
            "Timelogs not found for {userid} between {start} and {end}".format(
                userid=userid, start=range_start, end=range_end
            )
        )




