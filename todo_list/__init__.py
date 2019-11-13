import os
import logging

from flask import Flask

from todo_list.helpers import generate_timestamp

logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(message)s",
    level=logging.DEBUG,
)


app = Flask(__name__)
# Workaround of "A secret key is required to use CSRF"error
SECRET_KEY = os.urandom(32)
TEMPLATES_AUTO_RELOAD = True
app.config.from_object(__name__)
app.add_template_global(generate_timestamp, name='timestamp')

from todo_list import api
from todo_list import views
