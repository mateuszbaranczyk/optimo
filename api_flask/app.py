import os
import time

from flask import Flask

MYSQL_USERNAME = os.getenv("MYSQL_USERNAME", "root")
MYSQL_ROOT_PASSWORD = os.getenv("MYSQL_ROOT_PASSWORD", "password")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "lib")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
MYSQL_HOST = os.getenv("MYSQL_HOST", "172.17.0.3")

DB_URI = f"mysql+pymysql://{MYSQL_USERNAME}:{MYSQL_ROOT_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"


def create_app(test_config=None):
    app = Flask("api_flask", instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI=DB_URI,
    )
    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from db import db

    time.sleep(10)  # wait for db...
    db.init_app(app)
    with app.app_context():
        db.create_all()

    from routes import api

    app.register_blueprint(api)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
