import json
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

@app.route(route="MyHttpTrigger", auth_level=func.AuthLevel.ANONYMOUS)
def main(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(
        json.dumps(todos),
        status_code=200,
        mimetype="application/json"
    )
