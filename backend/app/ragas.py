"""
Carnatic raga definitions with swara → western note mapping.

Swaras are expressed in Carnatic notation (S, R2, G3, M1, M2, P, D2, N3).
Western note equivalents assume Sa = C (Middle C / MIDI 60).
"""

from typing import TypedDict


# ---------------------------------------------------------------------------
# Types
# ---------------------------------------------------------------------------

class RagaDefinition(TypedDict):
    name: str
    arohanam: list[str]
    avarohanam: list[str]
    vadi: str
    samavadi: str


# ---------------------------------------------------------------------------
# Swara → Western note mapping (Sa = C)
# ---------------------------------------------------------------------------

SWARA_TO_WESTERN: dict[str, str] = {
    "S":  "C",
    "R2": "D",
    "G3": "E",
    "M1": "F",
    "M2": "F#",
    "P":  "G",
    "D2": "A",
    "N3": "B",
}


# ---------------------------------------------------------------------------
# Raga definitions
# ---------------------------------------------------------------------------

RAGAS: dict[str, RagaDefinition] = {
    "shankarabharanam": {
        "name": "Shankarabharanam",
        "arohanam":   ["S", "R2", "G3", "M1", "P", "D2", "N3", "S"],
        "avarohanam": ["S", "N3", "D2", "P",  "M1", "G3", "R2", "S"],
        "vadi":    "G3",
        "samavadi": "N3",
    },
    "kalyani": {
        "name": "Kalyani",
        "arohanam":   ["S", "R2", "G3", "M2", "P", "D2", "N3", "S"],
        "avarohanam": ["S", "N3", "D2", "P",  "M2", "G3", "R2", "S"],
        "vadi":    "M2",
        "samavadi": "S",
    },
    "mohanam": {
        "name": "Mohanam",
        "arohanam":   ["S", "R2", "G3", "P", "D2", "S"],
        "avarohanam": ["S", "D2", "P",  "G3", "R2", "S"],
        "vadi":    "G3",
        "samavadi": "D2",
    },
    "hamsadhwani": {
        "name": "Hamsadhwani",
        "arohanam":   ["S", "R2", "G3", "P", "N3", "S"],
        "avarohanam": ["S", "N3", "P",  "G3", "R2", "S"],
        "vadi":    "G3",
        "samavadi": "N3",
    },
}


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def get_raga(name: str) -> RagaDefinition | None:
    """Return a raga definition by its key (e.g. 'kalyani'), or None."""
    return RAGAS.get(name.lower())


def get_raga_notes(name: str) -> list[str] | None:
    """
    Return the unique western notes used by a raga, derived from both
    arohanam and avarohanam (preserving arohanam order, deduped).
    Returns None if the raga is not found.
    """
    raga = get_raga(name)
    if raga is None:
        return None

    seen: set[str] = set()
    notes: list[str] = []
    for swara in raga["arohanam"] + raga["avarohanam"]:
        western = SWARA_TO_WESTERN.get(swara)
        if western and western not in seen:
            seen.add(western)
            notes.append(western)
    return notes


def get_all_ragas() -> list[dict]:
    """Return all ragas as a list of dicts with 'id' injected."""
    return [{"id": key, **value} for key, value in RAGAS.items()]
