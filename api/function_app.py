import json
import os
from uuid import uuid4
import azure.functions as func

app = func.FunctionApp()

todos = [
    {"id": 1, "task": "Learn Azure Functions with Python"},
    {"id": 2, "task": "Build Vue frontend"},
    {"id": 3, "task": "Deploy to Azure"},
    {"id": 4, "task": "Celebrate!"},
    {"id": 5, "task": "Write documentation"},
    {"id": 6, "task": "Demonstrate to team"},
]

@app.route(route="MyHttpTrigger", auth_level=func.AuthLevel.ANONYMOUS, methods=["GET"])
def main(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(
        json.dumps(todos),
        status_code=200,
        mimetype="application/json"
    )

@app.route(route="MyHttpTrigger", auth_level=func.AuthLevel.ANONYMOUS, methods=["POST"])
def add_todo(req: func.HttpRequest) -> func.HttpResponse:
  try:
    req_body = req.get_json()
    new_todo = {
      "id": max(todo["id"] for todo in todos) + 1,
      "task": req_body.get("task")
    }
    todos.append(new_todo)
    return func.HttpResponse(
      json.dumps(new_todo),
      status_code=201,
      mimetype="application/json"
    )
  except ValueError:
    return func.HttpResponse("Invalid request body", status_code=400)


# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# JSON_FILE = os.path.join(BASE_DIR, 'todos.json')

# def read_todos():
#     with open(JSON_FILE, 'r') as f:
#         return json.load(f)

# def write_todos(todos):
#   with open(JSON_FILE, 'w') as f:
#     json.dump(todos, f, indent=2)

# @app.route(route="MyHttpTrigger", auth_level=func.AuthLevel.ANONYMOUS, methods=["GET", "POST"])
# def main(req: func.HttpRequest) -> func.HttpResponse:
#     todos = read_todos()

#     if req.method == "POST":
#         todo = {
#            "id": max([t["id"] for t in todos], default=0) + 1,
#             **req.get_json()
#         }
#         todos.append(todo)
#         write_todos(todos)

#     return func.HttpResponse(
#         json.dumps(todos),
#         status_code=200,
#         mimetype="application/json"
#     )
