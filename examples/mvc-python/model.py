"""Estado, validação e persistência. Não conhece HTTP ou HTML."""
from contextlib import closing
from dataclasses import dataclass
import sqlite3

@dataclass(frozen=True)
class Task:
    id: int
    title: str

class TaskStore:
    def __init__(self, database: str):
        self.database = database
        with closing(sqlite3.connect(database)) as db:
            with db:
                db.execute("CREATE TABLE IF NOT EXISTS tasks "
                           "(id INTEGER PRIMARY KEY, title TEXT NOT NULL)")

    def list_tasks(self) -> list[Task]:
        with closing(sqlite3.connect(self.database)) as db:
            rows = db.execute("SELECT id, title FROM tasks ORDER BY id").fetchall()
        return [Task(id=row[0], title=row[1]) for row in rows]

    def create_task(self, title: object) -> Task:
        if not isinstance(title, str) or not title.strip():
            raise ValueError("O título deve ser uma string não vazia.")
        title = title.strip()
        if len(title) > 200:
            raise ValueError("O título deve ter no máximo 200 caracteres.")
        with closing(sqlite3.connect(self.database)) as db:
            with db:
                cursor = db.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
                task_id = cursor.lastrowid
        return Task(id=task_id, title=title)
