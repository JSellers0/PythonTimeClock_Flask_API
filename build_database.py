import os
from config import db
from models import User, Client, Project, Timelog

if os.path.exists("timeclock.sqlite"):
    os.remove("timeclock.sqlite")

db.create_all()