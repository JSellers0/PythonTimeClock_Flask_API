import os
from config import db, bc
from models import User, Project, Task, Note, Timelog

if os.path.exists("timeclock.sqlite"):
    os.remove("timeclock.sqlite")

db.create_all()

os.chown("timeclock.sqlite", 48, 48)

os.chmod("timeclock.sqlite", 0o664)

# Add some test data
user = User(
    user_name="user1",
    email="user1@test.com",
    encoded_password=bc.generate_password_hash("user1").decode("utf-8")
)

project = Project(project_name="General Overhead")

task = Task(task_name="Admin")

note = Note(note_name="Work Order Training")

db.session.add(user)
db.session.add(project)
db.session.add(task)
db.session.add(note)
db.session.commit()