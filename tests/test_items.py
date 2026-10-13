from fastapi.testclient import TestClient

from app.database import create_database
from app.main import create_app


def test_item_crud(tmp_path):
    app = create_app(f"sqlite:///{tmp_path / 'test.db'}")

    with TestClient(app) as client:
        created = client.post(
            "/items", json={"name": "Notebook", "description": "Grid paper"}
        )
        assert created.status_code == 201
        item = created.json()
        assert item["name"] == "Notebook"

        listed = client.get("/items")
        assert listed.status_code == 200
        assert listed.json() == [item]

        updated = client.put(
            f"/items/{item['id']}", json={"name": "Journal", "description": None}
        )
        assert updated.status_code == 200
        assert updated.json()["name"] == "Journal"

        deleted = client.delete(f"/items/{item['id']}")
        assert deleted.status_code == 204
        assert client.get(f"/items/{item['id']}").status_code == 404


def test_database_url_loaded_from_dotenv(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("DATABASE_URL", raising=False)
    database_path = (tmp_path / "configured.db").as_posix()
    (tmp_path / ".env").write_text(f"DATABASE_URL=sqlite:///{database_path}\n")

    engine, _ = create_database()

    assert engine.url.database == database_path
    engine.dispose()