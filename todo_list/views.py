from flask import render_template

from todo_list import app
from todo_list import db_utils

@app.route('/items/all')
def show_all_items():
    res_data = db_utils.get_all_items()

    return render_template(
        'index.html',
        items=res_data['items']
    )
