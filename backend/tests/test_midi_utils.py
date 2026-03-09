import os
import pytest
from app.midi_utils import note_to_midi, swara_to_midi, create_midi, build_midi_bytes


def test_note_to_midi_mapping():
    assert note_to_midi("C") == 60
    assert note_to_midi("D") == 62
    assert note_to_midi("E") == 64
    assert note_to_midi("F") == 65
    assert note_to_midi("F#") == 66
    assert note_to_midi("G") == 67
    assert note_to_midi("A") == 69
    assert note_to_midi("B") == 71


def test_note_to_midi_unknown_raises():
    with pytest.raises(ValueError):
        note_to_midi("X")


def test_swara_to_midi():
    assert swara_to_midi("S") == 60
    assert swara_to_midi("P") == 67
    assert swara_to_midi("G3") == 64


def test_swara_to_midi_unknown_raises():
    with pytest.raises(ValueError):
        swara_to_midi("ZZ")


def test_create_midi_returns_path(tmp_path, monkeypatch):
    import app.midi_utils as mu
    monkeypatch.setattr(mu, "GENERATED_DIR", tmp_path)
    path = create_midi(["C", "D", "E"], instrument_program=0, tempo=90)
    assert os.path.exists(path)
    assert path.endswith(".mid")
    assert os.path.getsize(path) > 0


def test_build_midi_bytes_returns_bytes():
    result = build_midi_bytes(notes=[60, 62, 64], tempo_bpm=90)
    assert isinstance(result, bytes)
    assert len(result) > 0
    assert result[:4] == b"MThd"  # MIDI file header
