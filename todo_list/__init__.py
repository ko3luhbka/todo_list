import os

from flask import Flask


app = Flask(__name__)
# workaround of 'A secret key is required to use CSRF'error
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

import todo_list.api
import todo_list.views