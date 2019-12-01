import logging
import sqlite3

from flask import (
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from todo_list.db_utils import query_db
from todo_list.forms import AddToDoTaskForm, UpdateStatusForm
from todo_list.todo_task import TaskStatus

app = current_app


@app.route('/tasks/all')
def show_all_tasks():
    """Show all todo list tasks"""
    all_tasks = query_db(query='SELECT * FROM tasks')
    return render_template('all_tasks.html', tasks=all_tasks)


@app.route('/tasks/new', methods=['GET', 'POST'])
def add_new_task():
    """Add new todo list task"""
    form = AddToDoTaskForm()
    if form.validate_on_submit():
        task = form.task.data
        logging.info("Inserting task '%s'", task)
        query_result = query_db(
            query='INSERT INTO tasks (task, status) VALUES (?, ?)',
            args=(task, TaskStatus.not_started.value),
            one=True,
        )

        # `fetchall()` returns empty list
        if query_result is None:
            flash(f"Task '{task}' was added successfuly")
            return redirect(url_for('show_all_tasks'))

        elif isinstance(query_result, sqlite3.IntegrityError):
            flash(
                "Error: task '{0}' already exists!".format(task),
                category='error',
            )

    logging.info(form.errors)
    return render_template('add_task.html', form=form)


@app.route('/tasks/update/<task_name>', methods=['GET', 'POST'])
def update_status(task_name):
    """Update todo list task status"""
    current_status = query_db(
        query='SELECT status FROM tasks WHERE task=?',
        args=(task_name,),
        one=True,
    )['status']
    form = UpdateStatusForm(status=TaskStatus(current_status).name)

    if request.method == 'GET':
        logging.info(
            'Current status of task [%s]: [%s]',
            task_name,
            current_status,
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
                "Status of task [%s] hasn't changed: [%s]",
                task_name,
                current_status,
            )
        else:
            logging.info(
                'New status of task [%s]: [%s]',
                task_name,
                new_status,
            )
            query_db(
                'UPDATE tasks SET status=? WHERE task=?',
                (new_status, task_name),
            )
            flash(f"The status of task '{task_name}' is set to '{new_status}'")

        return redirect(url_for('show_all_tasks'))


@app.route('/tasks/delete/<task_name>')
def delete_task(task_name):
    """Delete todo list task"""
    query_db('DELETE FROM tasks WHERE task=?', (task_name,), one=True)
    flash(f"Task '{task_name}' was deleted successfuly")

    return redirect(url_for('show_all_tasks'))
