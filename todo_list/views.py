from flask import (
    render_template, 
    redirect, 
    request, 
    flash,
    get_flashed_messages,
    url_for,
)

from todo_list import app
from todo_list import db_utils
from todo_list.forms import AddToDoTaskForm


@app.route('/items/all')
def show_all_tasks():
    res_data = db_utils.get_all_items()

    return render_template(
        'all_items.html',
        items=res_data['items']
    )


@app.route('/items/new', methods=['GET', 'POST'])
def add_new_task():
    form = AddToDoTaskForm()
    if form.validate_on_submit():
        task = form.item.data
        db_utils.add_item(task)
        flash(f"Task '{task}' was added successfuly")
        return render_template(
            'all_items.html',
            form=form
        )
    
    print(form.errors)
    return render_template(
        'add_item.html',
        form=form
    )
