"""
Preset tune definitions — well-known melodies stored as note sequences.

Notes use octave-qualified format (e.g. "C4", "F#4", "D5").
Each preset includes a suggested tempo for best playback.
"""

from typing import TypedDict


class PresetDefinition(TypedDict):
    name: str
    category: str
    description: str
    notes: list[str]
    tempo: int


PRESETS: dict[str, PresetDefinition] = {
    "happy_birthday": {
        "name": "Happy Birthday",
        "category": "Celebration",
        "description": "The classic birthday song",
        "notes": [
            "D4", "D4", "E4", "D4", "G4", "F#4",
            "D4", "D4", "E4", "D4", "A4", "G4",
            "D4", "D4", "D5", "B4", "G4", "F#4", "E4",
            "C5", "C5", "B4", "G4", "A4", "G4",
        ],
        "tempo": 100,
    },
    "twinkle_twinkle": {
        "name": "Twinkle Twinkle Little Star",
        "category": "Classic",
        "description": "The beloved nursery rhyme melody",
        "notes": [
            "C4", "C4", "G4", "G4", "A4", "A4", "G4",
            "F4", "F4", "E4", "E4", "D4", "D4", "C4",
            "G4", "G4", "F4", "F4", "E4", "E4", "D4",
            "G4", "G4", "F4", "F4", "E4", "E4", "D4",
            "C4", "C4", "G4", "G4", "A4", "A4", "G4",
            "F4", "F4", "E4", "E4", "D4", "D4", "C4",
        ],
        "tempo": 90,
    },
    "jana_gana_mana": {
        "name": "Jana Gana Mana",
        "category": "Indian Patriotic",
        "description": "Indian National Anthem — opening lines",
        "notes": [
            "C4", "D4", "E4", "E4", "E4", "E4", "E4",
            "F4", "E4", "D4", "E4", "D4", "C4",
            "C4", "D4", "E4", "E4", "E4", "E4",
            "E4", "F4", "E4", "D4", "C4", "D4", "E4",
            "D4", "E4", "F4", "F4", "F4", "E4", "D4",
            "E4", "C4",
        ],
        "tempo": 80,
    },
    "vande_mataram": {
        "name": "Vande Mataram",
        "category": "Indian Patriotic",
        "description": "India's national song — opening phrase",
        "notes": [
            "C4", "D4", "E4", "C4", "D4", "E4",
            "G4", "E4", "D4", "C4",
            "C4", "D4", "E4", "D4", "C4", "A3",
            "C4", "D4", "C4",
            "C4", "D4", "E4", "C4", "D4", "E4",
            "G4", "E4", "D4", "C4",
        ],
        "tempo": 85,
    },
    "ode_to_joy": {
        "name": "Ode to Joy",
        "category": "Classical Western",
        "description": "Beethoven's Symphony No. 9 — main theme",
        "notes": [
            "E4", "E4", "F4", "G4", "G4", "F4", "E4", "D4",
            "C4", "C4", "D4", "E4", "E4", "D4", "D4",
            "E4", "E4", "F4", "G4", "G4", "F4", "E4", "D4",
            "C4", "C4", "D4", "E4", "D4", "C4", "C4",
        ],
        "tempo": 95,
    },
    "saare_jahan_se_accha": {
        "name": "Saare Jahan Se Accha",
        "category": "Indian Patriotic",
        "description": "Iconic Indian patriotic song by Iqbal",
        "notes": [
            "E4", "E4", "E4", "D4", "C4",
            "D4", "E4", "F4", "E4",
            "G4", "G4", "G4", "F4", "E4",
            "F4", "G4", "A4", "G4",
            "E4", "E4", "D4", "C4",
            "D4", "E4", "D4", "C4",
        ],
        "tempo": 90,
    },
    "raghupati_raghav": {
        "name": "Raghupati Raghav Raja Ram",
        "category": "Indian Devotional",
        "description": "Popular devotional bhajan associated with Mahatma Gandhi",
        "notes": [
            "G4", "G4", "A4", "G4", "E4",
            "G4", "A4", "G4",
            "E4", "E4", "D4", "C4", "D4", "E4",
            "G4", "G4", "A4", "G4", "E4",
            "G4", "A4", "G4",
            "E4", "D4", "C4", "C4",
        ],
        "tempo": 85,
    },
    "sa_re_ga_ma": {
        "name": "Sa Re Ga Ma Scale",
        "category": "Carnatic Practice",
        "description": "Ascending and descending Carnatic scale exercise",
        "notes": [
            "C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5",
            "C5", "B4", "A4", "G4", "F4", "E4", "D4", "C4",
            "C4", "E4", "G4", "C5",
            "C5", "G4", "E4", "C4",
        ],
        "tempo": 80,
    },
    "mohanam_alapana": {
        "name": "Mohanam Alapana",
        "category": "Carnatic Practice",
        "description": "A melodic phrase exploration in Raga Mohanam",
        "notes": [
            "C4", "D4", "E4", "G4", "A4", "G4", "E4", "D4",
            "C4", "D4", "G4", "A4", "C5", "A4", "G4",
            "E4", "G4", "E4", "D4", "C4",
            "D4", "E4", "G4", "A4", "G4", "E4", "D4", "C4",
        ],
        "tempo": 75,
    },
    "kalyani_varnam": {
        "name": "Kalyani Varnam",
        "category": "Carnatic Practice",
        "description": "A short phrase in Raga Kalyani (Yaman equivalent)",
        "notes": [
            "C4", "D4", "E4", "F#4", "G4", "A4", "B4", "C5",
            "B4", "A4", "G4", "F#4", "E4", "D4", "C4",
            "E4", "F#4", "G4", "A4", "B4", "A4", "G4", "F#4",
            "E4", "D4", "E4", "F#4", "G4",
        ],
        "tempo": 80,
    },
}


def get_all_presets() -> list[dict]:
    return [
        {
            "id": key,
            "name": val["name"],
            "category": val["category"],
            "description": val["description"],
            "tempo": val["tempo"],
            "note_count": len(val["notes"]),
        }
        for key, val in PRESETS.items()
    ]


def get_preset(preset_id: str) -> PresetDefinition | None:
    return PRESETS.get(preset_id)
