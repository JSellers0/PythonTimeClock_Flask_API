"""
This is the note module and supports all REST actions for the note table
"""
from flask import abort
from models import Note, NoteSchema
from config import db

def read_all():
    notes = Note.query.order_by(Note.note_name).all()

    note_schema = NoteSchema(many=True)
    data = note_schema.dump(notes)
    return data

# ToDo: Add read_user: Note.join(user_note_exclude).all()
def read_one(noteid):
    note = Note.query.filter(Note.noteid == noteid).one_or_none()

    if note is not None:
        note_schema = NoteSchema()
        data = note_schema.dump(note)
        return data, 200
    else:
        abort(
            404,
            "Note Record not found for {}".format(noteid)
        )

def create(note_name):
    existing_note = Note.query.filter(Note.note_name == note_name).one_or_none()

    if existing_note is None:
        schema = NoteSchema()
        new_note = schema.load({"note_name": note_name}, session=db.session)

        db.session.add(new_note)
        db.session.commit()

        data = schema.dump(new_note)

        return data, 201

    else:
        abort(
            409,
            "Note {} already exists.".format(note_name)
        )

def update(noteid, note):
    update_note = Note.query.filter(Note.noteid == noteid).one_or_none()

    new_note_name = note.get("note_name")
    existing_note = Note.query.filter(Note.note_name == new_note_name).one_or_none()

    if update_note is None:
        abort(
            404, 
            "Note not found for ID {}.".format(noteid)
        )
    elif existing_note is not None:
        abort(
            409,
            "Note {} already exists.".format(new_note_name)
        )
    else:
        schema = NoteSchema()
        update = schema.load(note, session=db.session)

        db.session.merge(update)
        db.session.commit()

        data = schema.dump(note)

        return data, 200


