import unittest
from unittest.mock import AsyncMock, patch
from httpx import AsyncClient, ASGITransport
from main import app


class TaskAppTestCase(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        transport = ASGITransport(app=app)
        self.client = AsyncClient(transport=transport, base_url="http://test")

    async def asyncTearDown(self):
        await self.client.aclose()

    async def test_auth_success(self):
        response = await self.client.post(
            "/auth/token",
            data={"username": "admin", "password": "admin123"},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.json())

    async def test_auth_fail(self):
        response = await self.client.post(
            "/auth/token",
            data={"username": "bad", "password": "wrong"},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        self.assertEqual(response.status_code, 401)

    async def test_create_task_requires_auth(self):
        response = await self.client.post(
            "/tasks",
            json={"assignee": "user1", "task_name": "test task"}
        )
        self.assertEqual(response.status_code, 401)

    @patch("tasks.service.TaskService.create_task", new_callable=AsyncMock)
    async def test_create_task_with_auth(self, mock_create_task):
        mock_create_task.return_value = {"id": "fake-task-id"}

        login = await self.client.post(
            "/auth/token",
            data={"username": "admin", "password": "admin123"},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        token = login.json()["access_token"]

        headers = {"Authorization": f"Bearer {token}"}
        response = await self.client.post(
            "/tasks",
            json={"assignee": "user1", "task_name": "test task"},
            headers=headers
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("id", data)
        self.assertEqual(data["id"], "fake-task-id")


if __name__ == "__main__":
    unittest.main()
