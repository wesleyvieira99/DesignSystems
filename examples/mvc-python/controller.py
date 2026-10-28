"""Interpreta a intenção e escolhe model e representação."""
from dataclasses import dataclass, field
from model import TaskStore
from views import json_response, task_json, task_page

@dataclass(frozen=True)
class Response:
    status: int
    body: bytes
    content_type: str = "application/json; charset=utf-8"
    headers: dict[str, str] = field(default_factory=dict)

class TaskController:
    def __init__(self, store: TaskStore):
        self.store = store

    def handle(self, method: str, path: str, data: dict | None = None) -> Response:
        if method == "GET" and path == "/":
            return Response(200, task_page(self.store.list_tasks()),
                            "text/html; charset=utf-8")
        if method == "GET" and path == "/api/tasks":
            return Response(200, json_response([task_json(t) for t in self.store.list_tasks()]))
        if method == "POST" and path in ("/tasks", "/api/tasks"):
            try:
                task = self.store.create_task((data or {}).get("title"))
            except ValueError as error:
                return Response(400, json_response({"error": str(error)}))
            if path == "/tasks":
                # Post/Redirect/Get evita reenvio ao atualizar a página.
                return Response(303, b"", headers={"Location": "/"})
            return Response(201, json_response(task_json(task)))
        return Response(404, json_response({"error": "Rota não encontrada."}))
