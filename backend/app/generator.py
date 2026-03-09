"""
Carnatic melody generator.

Generates a random note sequence constrained to a raga's allowed notes,
converts it to a MIDI file, and returns a structured result.
"""

import random

from app.ragas import get_raga_notes
from app.instruments import get_instrument
from app.midi_utils import create_midi


class GenerationError(Exception):
    pass


def generate_composition(
    raga_name: str,
    instrument_name: str,
    tempo: int = 90,
    length: int = 32,
) -> dict:
    """
    Generate a random melody within the given raga and write it to a MIDI file.

    Args:
        raga_name:       Raga key (e.g. "mohanam")
        instrument_name: Instrument name (e.g. "veena")
        tempo:           BPM
        length:          Number of notes in the generated melody

    Returns:
        {
            "raga":       raga_name,
            "instrument": instrument_name,
            "notes":      [...],
            "midi_file":  "/abs/path/to/file.mid"
        }

    Raises:
        GenerationError: if the raga is not found
    """
    allowed_notes = get_raga_notes(raga_name)
    if allowed_notes is None:
        raise GenerationError(f"Unknown raga: {raga_name!r}")

    melody = [random.choice(allowed_notes) for _ in range(length)]

    midi_program = get_instrument(instrument_name)
    midi_path = create_midi(melody, midi_program, tempo)

    return {
        "raga":       raga_name,
        "instrument": instrument_name,
        "notes":      melody,
        "midi_file":  midi_path,
    }
