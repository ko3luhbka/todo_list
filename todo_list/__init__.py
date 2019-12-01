import logging
import os

from flask import Flask

from todo_list.helpers import generate_timestamp

logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(message)s",
    level=logging.DEBUG,
)

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        DATABASE = os.path.join(app.instance_path, 'todo.db'),
        TEMPLATES_AUTO_RELOAD = True
    )
    app.add_template_global(generate_timestamp, name='timestamp')

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    with app.app_context():
        
        from todo_list import api, views

    return app