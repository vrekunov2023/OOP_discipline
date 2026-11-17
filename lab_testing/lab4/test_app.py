import json
import sqlite3

import pytest

from app import create_app, export_tasks


@pytest.fixture
def resources(tmp_path):
    db_path = tmp_path / "tasks.db"
    export_path = tmp_path / "tasks.json"

    app = create_app(db_path, export_path)
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client, db_path, export_path


def read_db(db_path):
    with sqlite3.connect(db_path) as connection:
        return connection.execute(
            "SELECT id, title FROM tasks ORDER BY id"
        ).fetchall()


def read_export(export_path):
    return json.loads(export_path.read_text(encoding="utf-8"))


def test_create_task(resources):
    client, db_path, export_path = resources

    response = client.post(
        "/tasks",
        json={"title": "Вивчити pytest"},
    )

    assert response.status_code == 201

    task = response.get_json()
    assert isinstance(task["id"], int)
    assert task["title"] == "Вивчити pytest"

    assert read_db(db_path) == [
        (task["id"], "Вивчити pytest"),
    ]
    assert read_export(export_path) == [task]


def test_get_tasks(resources):
    client, _, _ = resources

    first = client.post(
        "/tasks",
        json={"title": "Перше завдання"},
    ).get_json()

    second = client.post(
        "/tasks",
        json={"title": "Друге завдання"},
    ).get_json()

    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.get_json() == [first, second]


def test_create_task_requires_title(resources):
    client, db_path, export_path = resources

    response = client.post("/tasks", json={})

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "Поле title є обов'язковим",
    }

    assert read_db(db_path) == []
    assert not export_path.exists()


def test_get_empty_tasks(resources):
    client, db_path, export_path = resources

    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.get_json() == []
    assert read_db(db_path) == []
    assert not export_path.exists()


def test_export_empty_tasks(resources):
    _, db_path, export_path = resources

    export_tasks(db_path, export_path)

    assert export_path.exists()
    assert read_export(export_path) == []
    assert read_db(db_path) == []


def test_two_tasks_order(resources):
    client, db_path, export_path = resources

    first_response = client.post(
        "/tasks",
        json={"title": "Перше завдання"},
    )
    second_response = client.post(
        "/tasks",
        json={"title": "Друге завдання"},
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 201

    first = first_response.get_json()
    second = second_response.get_json()

    assert first["id"] < second["id"]

    assert read_db(db_path) == [
        (first["id"], "Перше завдання"),
        (second["id"], "Друге завдання"),
    ]

    assert read_export(export_path) == [first, second]


def test_corrupted_json_is_replaced(resources):
    client, db_path, export_path = resources

    export_path.write_text(
        '{"tasks": пошкоджений JSON',
        encoding="utf-8",
    )

    with pytest.raises(json.JSONDecodeError):
        read_export(export_path)

    response = client.post(
        "/tasks",
        json={"title": "Відновлення експорту"},
    )

    assert response.status_code == 201

    task = response.get_json()

    assert read_db(db_path) == [
        (task["id"], "Відновлення експорту"),
    ]
    assert read_export(export_path) == [task]


def test_delete_task(resources):
    client, db_path, export_path = resources

    first = client.post(
        "/tasks",
        json={"title": "Видалити"},
    ).get_json()

    second = client.post(
        "/tasks",
        json={"title": "Залишити"},
    ).get_json()

    response = client.delete(f"/tasks/{first['id']}")

    assert response.status_code == 200
    assert response.get_json() == {"deleted": first["id"]}

    assert read_db(db_path) == [
        (second["id"], "Залишити"),
    ]
    assert read_export(export_path) == [second]

    get_response = client.get("/tasks")
    assert get_response.status_code == 200
    assert get_response.get_json() == [second]


def test_delete_last_task(resources):
    client, db_path, export_path = resources

    task = client.post(
        "/tasks",
        json={"title": "Єдине завдання"},
    ).get_json()

    response = client.delete(f"/tasks/{task['id']}")

    assert response.status_code == 200
    assert response.get_json() == {"deleted": task["id"]}

    assert read_db(db_path) == []
    assert read_export(export_path) == []


def test_delete_unknown_task(resources):
    client, db_path, export_path = resources

    task = client.post(
        "/tasks",
        json={"title": "Зберегти завдання"},
    ).get_json()

    response = client.delete(f"/tasks/{task['id'] + 1}")

    assert response.status_code == 404
    assert response.get_json() == {
        "error": "Завдання не знайдено",
    }

    assert read_db(db_path) == [
        (task["id"], "Зберегти завдання"),
    ]
    assert read_export(export_path) == [task]