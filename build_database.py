import os
from config import db, bc
from models import User, Client, Project, Timelog

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

client = Client(client_name="Test Client")

project = Project(project_name="Test Project")

db.session.add(user)
db.session.add(client)
db.session.add(project)
db.session.commit()