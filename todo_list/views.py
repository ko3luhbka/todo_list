import logging

from flask import current_app, flash, render_template, request

from todo_list.db_utils import QueryDB
from todo_list.forms import AddToDoTaskForm, UpdateStatusForm
from todo_list.todo_task import TaskStatus

app = current_app
db = QueryDB()

@app.route("/tasks/all")
def show_all_tasks():
    """Show all todo list tasks"""
    query_result = db.get_all_tasks()

    return render_template(
        "all_tasks.html",
        tasks=query_result["tasks"],
    )


@app.route("/tasks/new", methods=["GET", "POST"])
def add_new_task():
    """Add new todo list task"""
    form = AddToDoTaskForm()
    if form.validate_on_submit():
        task = form.task.data
        query_result = db.add_task(task)
        if isinstance(query_result, dict):
            flash(f"Task '{task}' was added successfuly")
        elif isinstance(query_result, str):
            flash(query_result, category='error')
        return render_template(
            "all_tasks.html",
            tasks=db.get_all_tasks()["tasks"],
        )
    logging.info(form.errors)
    return render_template(
        "add_task.html",
        form=form,
    )


@app.route("/tasks/update/<task_name>", methods=["GET", "POST"])
def update_status(task_name):
    """Update todo list task status"""
    current_status = db.get_task(task_name)
    form = UpdateStatusForm(status=TaskStatus(current_status).name)

    if request.method == "GET":
        logging.info(
            "Current status of task [%s]: [%s]",
            task_name,
            current_status,
        )
        return render_template(
            "update_status.html",
            form=form,
            task_name=task_name,
        )

    if request.method == "POST":
        new_status = TaskStatus[form.status.data].value
        if new_status == current_status:
            logging.info(
                "Status of task [%s] didnt change: [%s]",
                task_name,
                current_status,
            )
        else:
            logging.info(
                "New status of task [%s]: [%s]",
                task_name,
                new_status,
            )
            db.update_status(
                task_name,
                new_status,
            )
            flash(f"The status of task '{task_name}' is set to '{new_status}'")

        return render_template(
            "all_tasks.html",
            tasks=db.get_all_tasks()["tasks"],
        )


@app.route("/tasks/delete/<task_name>")
def delete_task(task_name):
    """Delete todo list task"""

    db.delete_task(task_name)
    flash(f"Task '{task_name}' was deleted successfuly")

    return render_template(
        "all_tasks.html",
        tasks=db.get_all_tasks()["tasks"]
    )
