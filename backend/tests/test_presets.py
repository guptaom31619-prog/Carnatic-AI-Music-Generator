from app.presets import get_all_presets, get_preset, PRESETS


def test_get_all_presets_count():
    result = get_all_presets()
    assert len(result) == len(PRESETS)


def test_all_presets_have_required_fields():
    for preset in get_all_presets():
        assert "id" in preset
        assert "name" in preset
        assert "category" in preset
        assert "tempo" in preset
        assert "note_count" in preset
        assert preset["note_count"] > 0


def test_get_preset_existing():
    preset = get_preset("happy_birthday")
    assert preset is not None
    assert preset["name"] == "Happy Birthday"
    assert len(preset["notes"]) > 0


def test_get_preset_unknown_returns_none():
    assert get_preset("nonexistent") is None


def test_all_presets_have_valid_notes():
    valid_bases = {"C", "D", "E", "F", "F#", "G", "A", "B"}
    for key, preset in PRESETS.items():
        for note in preset["notes"]:
            base = note.rstrip("0123456789")
            assert base in valid_bases, f"Invalid note {note!r} in preset {key!r}"
