from app.instruments import get_instrument, get_all_instruments


def test_get_all_instruments():
    instruments = get_all_instruments()
    assert "veena" in instruments
    assert "violin" in instruments
    assert "flute" in instruments
    assert "mridangam" in instruments
    assert "piano" in instruments


def test_get_instrument_known():
    assert get_instrument("veena") == 24
    assert get_instrument("violin") == 40
    assert get_instrument("flute") == 73
    assert get_instrument("mridangam") == 115
    assert get_instrument("piano") == 0


def test_get_instrument_case_insensitive():
    assert get_instrument("Veena") == 24
    assert get_instrument("VIOLIN") == 40


def test_get_instrument_unknown_defaults_to_piano():
    assert get_instrument("sitar") == 0
    assert get_instrument("unknown") == 0
