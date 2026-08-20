"""Unit tests for the TaskFlow API, using Flask's test client and a temp database."""

import tempfile
import unittest
from pathlib import Path

from app import create_app


class TaskFlowApiTests(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        db_path = Path(self.tmp_dir.name) / "test.db"
        app = create_app(db_path=db_path)
        app.config.update(TESTING=True)
        self.client = app.test_client()

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_health(self):
        res = self.client.get("/api/health")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json(), {"status": "ok"})

    def test_empty_task_list(self):
        res = self.client.get("/api/tasks")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json(), [])

    def test_create_task_requires_title(self):
        res = self.client.post("/api/tasks", json={"priority": "high"})
        self.assertEqual(res.status_code, 400)

    def test_create_task_rejects_bad_priority(self):
        res = self.client.post("/api/tasks", json={"title": "Test", "priority": "urgent"})
        self.assertEqual(res.status_code, 400)

    def test_create_and_fetch_task(self):
        res = self.client.post("/api/tasks", json={"title": "Write tests", "priority": "high"})
        self.assertEqual(res.status_code, 201)
        created = res.get_json()
        self.assertEqual(created["title"], "Write tests")
        self.assertEqual(created["status"], "todo")

        res = self.client.get(f"/api/tasks/{created['id']}")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()["title"], "Write tests")

    def test_get_missing_task_returns_404(self):
        res = self.client.get("/api/tasks/9999")
        self.assertEqual(res.status_code, 404)

    def test_update_task_status(self):
        created = self.client.post("/api/tasks", json={"title": "Ship feature"}).get_json()
        res = self.client.patch(f"/api/tasks/{created['id']}", json={"status": "doing"})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()["status"], "doing")

    def test_update_task_rejects_bad_status(self):
        created = self.client.post("/api/tasks", json={"title": "Ship feature"}).get_json()
        res = self.client.patch(f"/api/tasks/{created['id']}", json={"status": "blocked"})
        self.assertEqual(res.status_code, 400)

    def test_delete_task(self):
        created = self.client.post("/api/tasks", json={"title": "Temp task"}).get_json()
        res = self.client.delete(f"/api/tasks/{created['id']}")
        self.assertEqual(res.status_code, 204)
        res = self.client.get(f"/api/tasks/{created['id']}")
        self.assertEqual(res.status_code, 404)

    def test_stats_endpoint(self):
        self.client.post("/api/tasks", json={"title": "A"})
        self.client.post("/api/tasks", json={"title": "B", "status": "done"})
        res = self.client.get("/api/tasks/stats")
        stats = res.get_json()
        self.assertEqual(stats["total"], 2)
        self.assertEqual(stats["done"], 1)
        self.assertEqual(stats["todo"], 1)

    def test_filter_by_status(self):
        self.client.post("/api/tasks", json={"title": "A", "status": "doing"})
        self.client.post("/api/tasks", json={"title": "B", "status": "done"})
        res = self.client.get("/api/tasks?status=doing")
        results = res.get_json()
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "A")

    def test_filter_rejects_bad_status(self):
        res = self.client.get("/api/tasks?status=nope")
        self.assertEqual(res.status_code, 400)


if __name__ == "__main__":
    unittest.main()
