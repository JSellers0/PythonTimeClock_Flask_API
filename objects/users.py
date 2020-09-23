"""
This is the User module and supports all REST actions for the user table
"""
from flask import abort, make_response
from models import User, UserSchema
from config import db, bc

def read_token(user):
    user_token = user.get("user_token")
    
    user = User.query.filter(User.user_token == user_token).one_or_none()

    if user is not None:
        user_schema = UserSchema(exclude=["userid", "user_token"])
        data = user_schema.dump(user)
        return data, 200
    else :
        abort(
            404,
            "User not found."
        )

def read_email(user):
    email = user.get("email")
    user = User.query.filter(User.email == email).one_or_none()

    if user is not None:
        user_schema = UserSchema(exclude=["encoded_password"])
        data = user_schema.dump(user)
        return data, 200
    else:
        abort(
            404,
            "User record not found for {}.".format(email)
        )

def create(user):
    user_name = user.get("user_name")
    email = user.get("email")
    token = user.get("user_token")
    timezone = user.get("timezone")

    existing_user = (
        User.query.filter(User.user_name == user_name)
        .filter(User.email == email)
        .one_or_none()
    )

    if existing_user is None:
        new_user = User(user_name, email, token, timezone)

        db.session.add(new_user)
        db.session.commit()

        dump_schema = UserSchema(exclude=["user_token"])

        data = dump_schema.dump(new_user)

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

        db.session.merge(update)
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
