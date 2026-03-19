import json
import os
from uuid import uuid4
import azure.functions as func

app = func.FunctionApp()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_FILE = os.path.join(BASE_DIR, 'todos.json')

def read_todos():
    with open(JSON_FILE, 'r') as f:
        return json.load(f)

def write_todos(todos):
  with open(JSON_FILE, 'w') as f:
    json.dump(todos, f, indent=2)

@app.route(route="MyHttpTrigger", auth_level=func.AuthLevel.ANONYMOUS, methods=["GET", "POST"])
def main(req: func.HttpRequest) -> func.HttpResponse:
    todos = read_todos()

    if req.method == "POST":
        todo = {
           "id": max([t["id"] for t in todos], default=0) + 1,
            **req.get_json()
        }
        todos.append(todo)
        write_todos(todos)

    return func.HttpResponse(
        json.dumps(todos),
        status_code=200,
        mimetype="application/json"
    )
