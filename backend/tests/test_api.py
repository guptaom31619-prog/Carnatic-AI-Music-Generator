from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    res = client.get("/")
    assert res.status_code == 200
    assert res.json() == {"message": "Carnatic AI Composer API running"}


def test_get_ragas():
    res = client.get("/ragas")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert "Shankarabharanam" in data
    assert "Kalyani" in data
    assert "Mohanam" in data
    assert "Hamsadhwani" in data


def test_get_instruments():
    res = client.get("/instruments")
    assert res.status_code == 200
    data = res.json()
    assert "Veena" in data
    assert "Piano" in data


def test_get_presets():
    res = client.get("/presets")
    assert res.status_code == 200
    data = res.json()
    assert len(data) >= 10
    names = [p["name"] for p in data]
    assert "Happy Birthday" in names


def test_get_preset_detail():
    res = client.get("/presets/happy_birthday")
    assert res.status_code == 200
    data = res.json()
    assert data["name"] == "Happy Birthday"
    assert len(data["notes"]) > 0


def test_get_preset_not_found():
    res = client.get("/presets/nonexistent")
    assert res.status_code == 404


def test_generate(tmp_path, monkeypatch):
    import app.midi_utils as mu
    monkeypatch.setattr(mu, "GENERATED_DIR", tmp_path)

    res = client.post("/generate", json={
        "raga": "Mohanam",
        "instrument": "Violin",
        "tempo": 90,
        "length": 8,
    })
    assert res.status_code == 200
    data = res.json()
    assert data["raga"] == "Mohanam"
    assert data["instrument"] == "Violin"
    assert len(data["notes"]) == 8
    assert data["midi_file"].endswith(".mid")


def test_generate_invalid_raga():
    res = client.post("/generate", json={
        "raga": "Nonexistent",
        "instrument": "Piano",
        "tempo": 90,
        "length": 8,
    })
    assert res.status_code == 400
