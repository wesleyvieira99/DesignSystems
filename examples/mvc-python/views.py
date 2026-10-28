"""Representações do estado. Não executam SQL."""
from dataclasses import asdict
from html import escape
import json
from model import Task

def json_response(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False).encode("utf-8")

def task_json(task: Task) -> dict:
    return asdict(task)

def task_page(tasks: list[Task]) -> bytes:
    items = "".join(f"<li>#{t.id} · {escape(t.title)}</li>" for t in tasks)
    html = f"""<!doctype html><html lang="pt-BR"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>MVC · System Atlas</title>
<style>body{{font:16px/1.7 system-ui;max-width:680px;margin:60px auto;padding:20px;
background:#10171a;color:#eef4f0}}h1{{font-size:40px;color:#c2ef8d}}
input,button{{font:inherit;padding:12px;border-radius:8px;border:1px solid #6d8072}}
input{{width:65%;background:#202b30;color:white}}button{{background:#c2ef8d}}
li{{padding:12px;border-bottom:1px solid #ffffff20}}a{{color:#c2ef8d}}
small{{color:#adc0b2}}</style>
<small>MODEL → CONTROLLER → VIEW / LABORATÓRIO LOCAL</small>
<h1>Uma tarefa. Três responsabilidades.</h1>
<form method="post" action="/tasks"><label for="title">Nova tarefa</label><br>
<input id="title" name="title" maxlength="200" required><button>Adicionar</button></form>
<ul>{items or '<li>Nenhuma tarefa ainda.</li>'}</ul>
<p><a href="/api/tasks">Ver a representação JSON</a></p>
<p><small>Exemplo educacional sem autenticação. Execute somente localmente.</small></p></html>"""
    return html.encode("utf-8")
