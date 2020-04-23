"""
This is the User module and supports all REST actions for the user table
"""
from flask import abort, make_response
from models import User, UserSchema
from config import db

def read_all():
    users = User.query.order_by(User.user_name).all()

    user_schema = UserSchema(many=True)
    data = user_schema.dump(users)
    return data

def read_one(userid):
    user = User.query.filter(User.userid == userid).one_or_none()

    if user is not None:
        user_schema = UserSchema()
        data = user_schema.dump(user)
        return data, 200
    else:
        abort(
            404,
            "User Record not found for {}".format(userid)
        )

def create(user):
    user_name = user.get("user_name")
    email = user.get("email")

    existing_user = (
        User.query.filter(User.user_name == user_name)
        .filter(User.email == email)
        .one_or_none()
    )

    if existing_user is None:
        schema = UserSchema()
        new_user = schema.load(user, session=db.session)

        db.session.add(new_user)
        db.session.commit()

        data = schema.dump(new_user)

        return data, 201

    else:
        abort(
            409,
            "User {user_name} at {email} already exists.".format(
                user_name=user_name, email=email)
        )

def update(userid, user):
    update_user = User.query.filter(User.userid == userid).one_or_none()

    user_name = user.get("user_name")
    email = user.get("email")

    existing_user = (
        User.query.filter(User.user_name == user_name)
        .filter(User.email == email)
        .one_or_none()
    )

    if update_user is None:
        abort(
            404,
            "User not found for Id: {}".format(userid)
        )
    elif existing_user is not None and existing_user.id != userid:
        abort(
            409,
            "User {user_name} at {email} already exists".format(
                user_name=user_name, email=email
            )
        )
    else:
        schema = UserSchema()
        update = schema.load(user, session=db.session)

        update.userid = update_user.userid

        db.session.merge(updat)
        db.session.commit()

        data = schema.dump(update_user)

        return data, 200

def delete(userid):
    user = User.query.filter(User.userid == userid).one_or_none()

    if user is not None:
        db.session.delete(user)
        db.session.commit()
        return make_response(
            "User {} deleted".format(userid), 200
        )
    else:
        abort(
            404,
            "User not found for Id: {}".format(userid)
        )