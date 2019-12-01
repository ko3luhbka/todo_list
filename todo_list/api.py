import json
import logging

from flask import Response, current_app, request

from todo_list.db_utils import QueryDB

db = QueryDB()
app = current_app

MIMETYPE = 'application/json'
HTTP_STATUS_OK = 200
HTTP_STATUS_NOT_FOUND = 404
HTTP_STATUS_BAD_REQUEST = 400


@app.route('/api/task/new', methods=['POST'])
def api_add_task() -> Response:
    """Add new todo list task"""

    req_data = request.get_json()
    task = req_data['task']

    res_data = db.add_task(task)
    logging.debug('res_data: %s', res_data)

    if res_data is None:
        return Response(
            "{'error': 'task is not added - ' + task + '}",
            status=HTTP_STATUS_BAD_REQUEST,
            mimetype=MIMETYPE,
        )
    return Response(
        json.dumps(res_data),
        mimetype=MIMETYPE,
    )


@app.route('/api/tasks/all')
def api_get_all_tasks():
    """Get all todo list tasks"""

    res_data = db.get_all_tasks()

    return Response(
        json.dumps(res_data),
        mimetype=MIMETYPE,
    )


@app.route('/api/task/status', methods=['GET'])
def api_get_task():
    """Get one todo list task by name"""

    task_name = request.args.get('name')
    status = db.get_task(task_name)

    if status is None:
        return Response(
            "{'error': 'task Not Found - %s'}" % task_name,
            status=HTTP_STATUS_NOT_FOUND,
            mimetype=MIMETYPE,
        )

    return Response(
        json.dumps({'status': status}),
        status=HTTP_STATUS_OK,
        mimetype=MIMETYPE,
    )


@app.route('/api/task/update', methods=['PUT'])
def api_update_status():
    """Update todo list task status"""

    req_data = request.get_json()
    task = req_data['task']

    status = req_data['status']

    res_data = db.update_status(task, status)

    if res_data is None:
        return Response(
            "{'error': 'Error updating task - ' + task + ', ' + status + '}",
            status=HTTP_STATUS_BAD_REQUEST,
            mimetype=MIMETYPE,
        )

    return Response(json.dumps(res_data), mimetype=MIMETYPE)


@app.route('/api/task/remove', methods=['DELETE'])
def api_delete_task():
    """Delete task by name"""

    req_data = request.get_json()
    task = req_data['task']

    res_data = db.delete_task(task)

    if res_data is None:
        return Response(
            "{'error': 'Error deleting task - ' + task + '}",
            status=HTTP_STATUS_BAD_REQUEST,
            mimetype=MIMETYPE,
        )

    return Response(json.dumps(res_data), mimetype=MIMETYPE)
