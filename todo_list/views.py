import logging

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
from todo_list.forms import (
    AddToDoTaskForm,
    UpdateStatusForm,
)
from todo_list.todo_task import TaskStatus


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
            items=db_utils.get_all_items()['items']
        )
    
    logging.info(form.errors)
    return render_template(
        'add_item.html',
        form=form
    )


@app.route('/items/update/<task_name>', methods=['GET', 'POST'])
def update_status(task_name):
    current_status = db_utils.get_item(task_name)
    form = UpdateStatusForm(status=TaskStatus(current_status).name)

    if request.method == 'GET':
        logging.info(
            'current status of item [%s]: [%s]',
            task_name,
            current_status
        )
        return render_template(
            'update_status.html',
            form=form,
            task_name=task_name,
        )

    if request.method == 'POST':
        new_status = TaskStatus[form.status.data].value
        if new_status == current_status:
            logging.info(
                'status of item [%s] didnt change: [%s]',
                task_name,
                current_status
            )
        else:
            logging.info(
                'new status of item [%s]: [%s]',
                task_name,
                new_status
                )
            db_utils.update_status(
                task_name,
                new_status
            )
            flash(f"The status of task '{task_name}' is set to '{new_status}'")
        
        return render_template(
            'all_items.html',
            items=db_utils.get_all_items()['items']
        )
    