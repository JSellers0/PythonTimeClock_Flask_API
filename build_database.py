import os
from config import db
from models import User, Client, Project, Timelog

if os.path.exists("timeclock.sqlite"):
    os.remove("timeclock.sqlite")

db.create_all()

os.chown("timeclock.sqlite", 48, 48)

os.chmod("timeclock.sqlite", 0o664)