from flask import Flask
import config

connex_app = config.connex_app

connex_app.add_api("swagger.yml")

@connex_app.route("/")
def home():
    return "Placeholder"

if __name__ == '__main__':
    connex_app.run(port=5001, debug=True)