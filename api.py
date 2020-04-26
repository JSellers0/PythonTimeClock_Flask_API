from flask import Flask
from flask_bcrypt import Bcrypt
import config

connex_app = config.connex_app
bcrypt = Bcrypt
bcrypt.init_app(connex_app)

connex_app.add_api("swagger.yml")

@connex_app.route("/")
def home():
    return "Placeholder"

if __name__ == '__main__':
    connex_app.run(debug=True)