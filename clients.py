"""
This is the client module and supports all REST actions for the client table
"""
from flask import abort
from models import Client, ClientSchema
from config import db

def read_all():
    clients = Client.query.order_by(Client.client_name).all()

    client_schema = ClientSchema(many=True)
    data = client_schema.dump(clients)
    return data

# ToDo: Add read_user: Client.join(user_client_exclude).all()

def read_one(clientid):
    client = Client.query.filter(Client.clientid == clientid).one_or_none()

    if client is not None:
        client_schema = ClientSchema()
        data = client_schema.dump(client)
    else:
        abort(
            404,
            "Client Record not found for {}".format(clientid)
        )

def create(client_name):
    existing_client = Client.query.filter(Client.client_name == client_name).one_or_none()

    if existing_client is None:
        schema = ClientSchema()
        new_client = schema.load(client, session=db.session)

        db.session.add(new_client)
        db.session.commit()

        data = schema.dump(new_client)

        return data, 201

    else:
        abort(
            409,
            "Client {} already exists.".format(client_name)
        )

