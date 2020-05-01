import os
import socket
from config import db, bc
from models import User, Project, Task, Note, Timelog

from datetime import datetime as dt

if os.path.exists("timeclock.sqlite"):
    os.remove("timeclock.sqlite")

db.create_all()

if "MacBook" not in socket.gethostname():
    os.chown("timeclock.sqlite", 48, 48)

    os.chmod("timeclock.sqlite", 0o664)

# Add some test data
user = User(
    user_name="user1",
    email="user1@test.com",
    encoded_password=bc.generate_password_hash("user1").decode("utf-8")
)

project = Project(project_name="general overhead")

task = Task(task_name="admin")

note = Note(note_name="work order training")

timelog = Timelog(
    userid=1,
    projectid=1,
    taskid=1,
    noteid=1,
    start=dt.strptime("2020-04-29 12:00:00", "%Y-%m-%d %H:%M:%S"),
    stop=dt.strptime("2020-04-29 13:00:00", "%Y-%m-%d %H:%M:%S")
)

db.session.add(user)
db.session.add(project)
db.session.add(task)
db.session.add(note)
db.session.add(timelog)
db.session.commit()

timelog = Timelog(
    userid=1,
    projectid=1,
    taskid=1,
    noteid=1,
    start=dt.strptime("2020-04-30 12:00:00", "%Y-%m-%d %H:%M:%S"),
    stop=dt.strptime("2020-04-30 13:00:00", "%Y-%m-%d %H:%M:%S")
)

db.session.add(timelog)
db.session.commit()