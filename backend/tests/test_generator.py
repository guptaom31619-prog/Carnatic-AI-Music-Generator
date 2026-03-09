import pytest
from app.generator import generate_composition, GenerationError


def test_generate_composition_basic(tmp_path, monkeypatch):
    import app.midi_utils as mu
    monkeypatch.setattr(mu, "GENERATED_DIR", tmp_path)

    result = generate_composition("mohanam", "veena", tempo=90, length=8)
    assert result["raga"] == "mohanam"
    assert result["instrument"] == "veena"
    assert len(result["notes"]) == 8
    assert result["midi_file"].endswith(".mid")

    allowed = {"C", "D", "E", "G", "A"}
    for note in result["notes"]:
        assert note in allowed, f"Note {note!r} not in Mohanam"


def test_generate_composition_different_lengths(tmp_path, monkeypatch):
    import app.midi_utils as mu
    monkeypatch.setattr(mu, "GENERATED_DIR", tmp_path)

    r16 = generate_composition("mohanam", "piano", length=16)
    r64 = generate_composition("mohanam", "piano", length=64)
    assert len(r16["notes"]) == 16
    assert len(r64["notes"]) == 64


def test_generate_composition_unknown_raga():
    with pytest.raises(GenerationError):
        generate_composition("nonexistent", "piano")


def test_generate_kalyani_has_f_sharp(tmp_path, monkeypatch):
    import app.midi_utils as mu
    monkeypatch.setattr(mu, "GENERATED_DIR", tmp_path)

    result = generate_composition("kalyani", "violin", length=64)
    assert "F" not in result["notes"]
    allowed = {"C", "D", "E", "F#", "G", "A", "B"}
    for note in result["notes"]:
        assert note in allowed
