import logging

from flask import (
    render_template,
    request,
    flash,
)

from todo_list import app
from todo_list import db_utils
from todo_list.forms import (
    AddToDoTaskForm,
    UpdateStatusForm,
)
from todo_list.todo_task import TaskStatus


@app.route("/tasks/all")
def show_all_tasks():
    """Show all todo list tasks"""

    res_data = db_utils.get_all_tasks()

    return render_template(
        "all_tasks.html",
        tasks=res_data["tasks"]
    )


@app.route("/tasks/new", methods=["GET", "POST"])
def add_new_task():
    """Add new todo list task"""

    form = AddToDoTaskForm()
    if form.validate_on_submit():
        task = form.task.data
        db_utils.add_task(task)
        flash(f"Task '{task}' was added successfuly")
        return render_template(
            "all_tasks.html",
            tasks=db_utils.get_all_tasks()["tasks"]
        )

    logging.info(form.errors)
    return render_template(
        "add_task.html",
        form=form,
    )


@app.route("/tasks/update/<task_name>", methods=["GET", "POST"])
def update_status(task_name):
    """Update todo list task status"""

    current_status = db_utils.get_task(task_name)
    form = UpdateStatusForm(status=TaskStatus(current_status).name)

    if request.method == "GET":
        logging.info(
            "current status of task [%s]: [%s]",
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
                "status of task [%s] didnt change: [%s]",
                task_name,
                current_status,
            )
        else:
            logging.info(
                "new status of task [%s]: [%s]",
                task_name,
                new_status,
            )
            db_utils.update_status(
                task_name,
                new_status,
            )
            flash(f"The status of task '{task_name}' is set to '{new_status}'")

        return render_template(
            "all_tasks.html",
            tasks=db_utils.get_all_tasks()["tasks"],
        )
