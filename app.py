import json
import os

from flask import Flask, request, Response
from werkzeug.exceptions import BadRequest

from tools import run_command

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


@app.post("/perform_query")
def perform_query() -> Response:
    try:
        data = json.loads(request.data)
        query = data["query"]
        file_name = data['file_name']

    except KeyError:
        raise BadRequest

    file_path = os.path.join(DATA_DIR, file_name)
    if not os.path.exists(file_path):
        raise BadRequest(description=f"Файл не найден")

    with open(file_path) as iter_obj:
        result = run_command(iter_obj, query)
        content = '\n'.join(result)
    return app.response_class(content, content_type="text/plain")
