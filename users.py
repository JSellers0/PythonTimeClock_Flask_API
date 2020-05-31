"""
This is the User module and supports all REST actions for the user table
"""
from flask import abort, make_response
from models import User, UserSchema
from config import db, bc

def read_name(user):
    user_name = user.get("user_name")
    sub_password = user.get("password")

    user = User.query.filter(User.user_name == user_name).one_or_none()

    if user is not None and bc.check_password_hash(user.encoded_password, sub_password):
        user_schema = UserSchema(exclude=["encoded_password"])
        data = user_schema.dump(user)
        return data, 200
    elif user is None:
        abort(
            404,
            "User record not found for {}.".format(user_name)
        )
    else :
        abort(
            404,
            "Incorrect password for {}.".format(user_name)
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
    # ToDo: Better handling of passwords between clients and server.
    """   
    Won't recognize hashes from applications.  Need to look into Authentication requests
    as intermediary improvement.  HTTPS + Authentication would be ultimate goal.
    """
    password = bc.generate_password_hash(user.get("password")).decode("utf-8")

    existing_user = (
        User.query.filter(User.user_name == user_name)
        .filter(User.email == email)
        .one_or_none()
    )

    if existing_user is None:
        schema = UserSchema()
        new_user = {
            "user_name": user_name,
            "email": email,
            "encoded_password": password
        }
        new_user = schema.load(new_user, session=db.session)

        db.session.add(new_user)
        db.session.commit()

        dump_schema = UserSchema(exclude=["encoded_password"])

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