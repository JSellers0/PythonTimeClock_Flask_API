import os
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__)))

# Create connexion app instance
connex_app = connexion.App(__name__, specification_dir=basedir)

# Get the Flask app instance
app = connex_app.app

sqlite_url = "sqlite:////" + os.path.join(basedir, "timeclock.sqlite")

app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = sqlite_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

ma = Marshmallow(app)

bc = Bcrypt(app)
    