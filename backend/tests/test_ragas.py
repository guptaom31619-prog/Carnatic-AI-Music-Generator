from app.ragas import get_raga, get_raga_notes, get_all_ragas, RAGAS


def test_get_all_ragas_returns_all():
    result = get_all_ragas()
    assert len(result) == len(RAGAS)
    assert all("id" in r and "name" in r for r in result)


def test_get_raga_existing():
    raga = get_raga("mohanam")
    assert raga is not None
    assert raga["name"] == "Mohanam"


def test_get_raga_case_insensitive():
    assert get_raga("Kalyani") is not None
    assert get_raga("KALYANI") is not None


def test_get_raga_unknown_returns_none():
    assert get_raga("nonexistent") is None


def test_mohanam_notes():
    notes = get_raga_notes("mohanam")
    assert notes == ["C", "D", "E", "G", "A"]


def test_kalyani_has_f_sharp():
    notes = get_raga_notes("kalyani")
    assert "F#" in notes
    assert "F" not in notes


def test_shankarabharanam_full_scale():
    notes = get_raga_notes("shankarabharanam")
    assert len(notes) == 7


def test_hamsadhwani_pentatonic():
    notes = get_raga_notes("hamsadhwani")
    assert notes == ["C", "D", "E", "G", "B"]


def test_raga_notes_unknown_returns_none():
    assert get_raga_notes("nonexistent") is None
