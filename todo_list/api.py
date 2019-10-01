import json
import logging
from flask import request, Response

from todo_list import db_utils
from todo_list import app

MIMETYPE = "application/json"
HTTP_STATUS_OK = 200
HTTP_STATUS_NOT_FOUND = 404
HTTP_STATUS_BAD_REQUEST = 400

@app.route("/api/task/new", methods=["POST"])
def add_task() -> Response:
    """Add new todo list task"""

    req_data = request.get_json()
    task = req_data["task"]

    res_data = db_utils.add_task(task)
    logging.debug("res_data: %s", res_data)

    if res_data is None:
        response = Response(
            "{'error': 'task is not added - " + task + "}",
            status=HTTP_STATUS_BAD_REQUEST,
            mimetype=MIMETYPE,
        )
    else:
        response = Response(
            json.dumps(res_data),
            mimetype=MIMETYPE,
        )
    return response


@app.route("/api/tasks/all")
def get_all_tasks():
    """Get all todo list tasks"""

    res_data = db_utils.get_all_tasks()
    
    return Response(
        json.dumps(res_data),
        mimetype=MIMETYPE,
    )


@app.route("/api/task/status", methods=["GET"])
def get_task():
    """Get one todo list task by name"""

    task_name = request.args.get("name")
    status = db_utils.get_task(task_name)

    if status is None:
        response = Response(
            "{'error': 'task Not Found - %s'}" % task_name,
            status=HTTP_STATUS_NOT_FOUND,
            mimetype=MIMETYPE,
        )
    else:
        res_data = {
            "status": status
        }

        response = Response(
            json.dumps(res_data),
            status=HTTP_STATUS_OK,
            mimetype=MIMETYPE,
        )

    return response


@app.route("/api/task/update", methods=["PUT"])
def update_status():
    """Update todo list task status"""

    req_data = request.get_json()
    task = req_data["task"]

    status = req_data["status"]

    res_data = db_utils.update_status(task, status)

    if res_data is None:
        response = Response(
            "{'error': 'Error updating task - " + task + ", " + status + "}",
            status=HTTP_STATUS_BAD_REQUEST,
            mimetype=MIMETYPE,
        )
    else:
        response = Response(json.dumps(res_data), mimetype=MIMETYPE)

    return response


@app.route("/api/task/remove", methods=["DELETE"])
def delete_task():
    """Delete task by name"""

    req_data = request.get_json()
    task = req_data["task"]

    res_data = db_utils.delete_task(task)

    if res_data is None:
        response = Response(
            "{'error': 'Error deleting task - " + task + "}",
            status=HTTP_STATUS_BAD_REQUEST,
            mimetype=MIMETYPE,
        )
    else:
        response = Response(json.dumps(res_data), mimetype=MIMETYPE)

    return response
