from datetime import datetime
from config import db, ma

""" ====== DATABASE ARCHITECTURE ====== """
# ToDo: Table Item State columns (ACT, INA, DEL) to allow soft and hard delete of table values.
# ToDo: Note Table, NoteID Field in Timelog to add notes, especially for projects that share activity code.
# ToDo: Update client/project names to match new time system

class User(db.Model):
    userid = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    encoded_password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return "User({}, {})".format(self.username, self.email)

class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
        sqla_session = db.session

class Client(db.Model):
    clientid = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return "Client({}, {})".format(self.clientid, self.client_name)

class ClientSchema(ma.ModelSchema):
    class Meta:
        model = Client
        sqla_session = db.session

class Project(db.Model):
    projectid = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return "project({}, {})".format(self.projectid, self.project_name)

class ProjectSchema(ma.ModelSchema):
    class Meta:
        model = Project
        sqla_session = db.session

class Timelog(db.Model):
    timelogid = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    stop = db.Column(db.DateTime)
    userid = db.Column(db.Integer, db.ForeignKey("user.userid"), nullable=False)
    clientid = db.Column(db.Integer, db.ForeignKey("client.clientid"), nullable=False)
    projectid = db.Column(db.Integer, db.ForeignKey("project.projectid"), nullable=False)

class TimelogSchema(ma.ModelSchema):
    class Meta:
        model = Timelog
        sqla_session = db.session
