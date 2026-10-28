import http.client
import json
from pathlib import Path
import tempfile
import threading
import unittest
from app import make_server
from controller import TaskController
from model import TaskStore
from views import task_page

class ModelAndControllerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = str(Path(self.temp.name) / "test.sqlite3")
        self.store = TaskStore(self.path)
        self.controller = TaskController(self.store)

    def test_validation_leaves_no_partial_record(self):
        for value in [None, " ", 42, "x" * 201]:
            with self.assertRaises(ValueError):
                self.store.create_task(value)
        self.assertEqual(self.store.list_tasks(), [])

    def test_persistence_and_parameterized_sql(self):
        title = "Robert'); DROP TABLE tasks;--"
        created = self.store.create_task(title)
        self.assertEqual(TaskStore(self.path).list_tasks(), [created])

    def test_html_escapes_user_text(self):
        self.store.create_task('<script>alert("x")</script>')
        body = task_page(self.store.list_tasks()).decode()
        self.assertIn("&lt;script&gt;", body)
        self.assertNotIn("<script>", body)

    def test_controller_representation_and_redirect(self):
        result = self.controller.handle("POST", "/api/tasks", {"title": "Aprender MVC"})
        self.assertEqual(result.status, 201)
        self.assertEqual(json.loads(result.body)["title"], "Aprender MVC")
        redirect = self.controller.handle("POST", "/tasks", {"title": "Ler CQRS"})
        self.assertEqual(redirect.status, 303)
        self.assertEqual(redirect.headers["Location"], "/")
        self.assertEqual(self.controller.handle("GET", "/missing").status, 404)

class HTTPTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.server = make_server(str(Path(cls.temp.name) / "http.sqlite3"), 0)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()
        cls.temp.cleanup()

    def request(self, method, path, body=None, media_type="application/json"):
        connection = http.client.HTTPConnection("127.0.0.1", self.server.server_port)
        try:
            connection.request(method, path, body=body, headers={"Content-Type": media_type})
            response = connection.getresponse()
            return response.status, response.read()
        finally:
            connection.close()

    def test_create_and_read_over_http(self):
        status, body = self.request("POST", "/api/tasks", '{"title":"Via HTTP"}')
        self.assertEqual(status, 201)
        status, body = self.request("GET", "/api/tasks")
        self.assertEqual(status, 200)
        self.assertTrue(any(t["title"] == "Via HTTP" for t in json.loads(body)))

    def test_invalid_json_and_media_type(self):
        self.assertEqual(self.request("POST", "/api/tasks", "{")[0], 400)
        self.assertEqual(self.request("POST", "/api/tasks", "[]")[0], 400)
        self.assertEqual(self.request("POST", "/api/tasks", "hello", "text/plain")[0], 415)
        self.assertEqual(self.request("POST", "/api/tasks", "x" * 4097)[0], 413)

if __name__ == "__main__":
    unittest.main()
