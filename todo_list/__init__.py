from flask import Flask

app = Flask(__name__)
import todo_list.api
import todo_list.views