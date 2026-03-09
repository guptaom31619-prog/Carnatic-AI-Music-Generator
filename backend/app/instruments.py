"""
Instrument definitions mapped to General MIDI program numbers.
Unknown instruments fall back to Piano (program 0).
"""

DEFAULT_INSTRUMENT = "piano"

INSTRUMENTS: dict[str, int] = {
    "veena":     24,   # Nylon Guitar — closest GM approximation
    "violin":    40,
    "flute":     73,
    "mridangam": 115,  # Woodblock — percussion approximation
    "piano":     0,
}


def get_instrument(name: str) -> int:
    """Return the GM program number for the instrument, defaulting to Piano."""
    return INSTRUMENTS.get(name.lower(), INSTRUMENTS[DEFAULT_INSTRUMENT])


def get_all_instruments() -> list[str]:
    """Return all available instrument names."""
    return list(INSTRUMENTS.keys())
