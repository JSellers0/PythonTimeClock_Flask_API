import os
import socket
from config import db, bc
from models import User, Project, Task, Note, Timelog

from datetime import datetime as dt

# ToDo: Add debug option to toggle test user and log creation.

if os.path.exists("timeclock.sqlite"):
    os.remove("timeclock.sqlite")

db.create_all()

if "MacBook" not in socket.gethostname():
    os.chown("timeclock.sqlite", 48, 48)

    os.chmod("timeclock.sqlite", 0o664)

# General Overhead Projects, Tasks, and Notes
db.session.add(Project(project_name="general overhead"))
db.session.add(Task(task_name="admin"))
db.session.add(Task(task_name="training"))
db.session.add(Task(task_name="general meeting"))
db.session.add(Note(note_name="general admin"))

# Absence Projects and Tasks
db.session.add(Project(project_name="paid absence us"))
db.session.add(Task(task_name="holiday pd"))
db.session.add(Task(task_name="mgr approved pd"))
db.session.add(Task(task_name="sick pd"))
db.session.add(Task(task_name="vacation pd"))

# Show Work Tasks
db.session.add(Task(task_name="reg-app dev 110.005"))
db.session.add(Task(task_name="ebs-general 230.001"))

# Commit real data in case we don't need test data
db.session.commit()

# Add some test data
db.session.add(User(
    user_name="user1",
    email="user1@test.com",
    encoded_password=bc.generate_password_hash("user1").decode("utf-8")
))

db.session.add(Timelog(
    userid=1,
    projectid=1,
    taskid=1,
    noteid=1,
    start=dt.strptime("2020-05-31 12:00:00", "%Y-%m-%d %H:%M:%S"),
    stop=dt.strptime("2020-05-31 13:00:00", "%Y-%m-%d %H:%M:%S")
))

db.session.add(Timelog(
    userid=1,
    projectid=1,
    taskid=1,
    noteid=1,
    start=dt.strptime("2020-05-31 14:00:00", "%Y-%m-%d %H:%M:%S"),
    stop=dt.strptime("2020-05-31 16:00:00", "%Y-%m-%d %H:%M:%S")
))

# Commit Test Data
db.session.commit()