import json
from flask import request, Response

from todo_list import db_utils
from todo_list import app


@app.route('/api/item/new', methods=['POST'])
def add_item() -> Response:
    req_data = request.get_json()
    item = req_data['item']

    res_data = db_utils.add_item(item)
    print(res_data)

    if res_data is None:
        response = Response(
            "{'error': 'Item is not added - " + item + "'}",
            status=400,
            mimetype='application/json'
        )
    else:
        response = Response(
            json.dumps(res_data),
            mimetype='application/json'
        )
    return response


@app.route('/api/items/all')
def get_all_items():
    res_data = db_utils.get_all_items()

    response = Response(
        json.dumps(res_data),
        mimetype='application/json'
    )
    return response


@app.route('/api/item/status', methods=['GET'])
def get_item():
    item_name = request.args.get('name')
    status = db_utils.get_item(item_name)

    if status is None:
        response = Response(
            "{'error': 'Item Not Found - %s'}" % item_name,
            status=404,
            mimetype='application/json'
        )
    else:
        res_data = {
            'status': status
        }

        response = Response(
            json.dumps(res_data),
            status=200,
            mimetype='application/json'
        )

    return response


@app.route('/api/item/update', methods=['PUT'])
def update_status():
    req_data = request.get_json()
    item = req_data['item']

    status = req_data['status']

    res_data = db_utils.update_status(item, status)

    if res_data is None:
        response = Response(
            "{'error': 'Error updating item - '" + item + ", " + status + "}",
            status=400,
            mimetype='application/json'
        )
    else:
        response = Response(json.dumps(res_data), mimetype='application/json')

    return response


@app.route('/api/item/remove', methods=['DELETE'])
def delete_item():
    req_data = request.get_json()
    item = req_data['item']

    res_data = db_utils.delete_item(item)

    if res_data is None:
        response = Response(
            "{'error': 'Error deleting item - '" + item + "}",
            status=400,
            mimetype='application/json'
        )
    else:
        response = Response(json.dumps(res_data), mimetype='application/json')

    return response
