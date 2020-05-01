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

class Task(db.Model):
    taskid = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return "Task({}, {})".format(self.taskid, self.task_name)

class TaskSchema(ma.ModelSchema):
    class Meta:
        model = Task
        sqla_session = db.session

class Note(db.Model):
    noteid = db.Column(db.Integer, primary_key=True)
    note_name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return "Note({}, {})".format(self.noteid, self.note_name)

class NoteSchema(ma.ModelSchema):
    class Meta:
        model = Note
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
    projectid = db.Column(db.Integer, db.ForeignKey("project.projectid"), nullable=False)
    taskid = db.Column(db.Integer, db.ForeignKey("task.taskid"), nullable=False)
    noteid = db.Column(db.Integer, db.ForeignKey("note.noteid"), nullable=False)

    def to_json(self):
        return {
            "timelogid": self.timelogid,
            "userid": self.userid,
            "projectid": self.projectid,
            "taskid": self.taskid,
            "noteid": self.noteid,
            "start": self.start,
            "stop": self.stop
        }

class TimelogSchema(ma.ModelSchema):
    class Meta:
        model = Timelog
        sqla_session = db.session
