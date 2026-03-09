"""
MIDI utility helpers.

Handles conversion between Carnatic swara notation and western note names
to MIDI note numbers, and MIDI file construction via mido.
"""

import time
from pathlib import Path

import mido

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEFAULT_ROOT_MIDI = 60  # Middle C = Sa
TICKS_PER_BEAT = 480
DEFAULT_VELOCITY = 80

GENERATED_DIR = Path(__file__).resolve().parent.parent / "generated"

# Western note name → absolute MIDI note number (octave 4, middle octave)
NOTE_TO_MIDI: dict[str, int] = {
    "C":  60,
    "D":  62,
    "E":  64,
    "F":  65,
    "F#": 66,
    "G":  67,
    "A":  69,
    "B":  71,
}

# Carnatic swara → semitone offset from Sa (Sa = C / MIDI 60)
SWARA_SEMITONES: dict[str, int] = {
    "S":  0,
    "R1": 1,  "R2": 2,  "R3": 3,
    "G1": 2,  "G2": 3,  "G3": 4,
    "M1": 5,  "M2": 6,
    "P":  7,
    "D1": 8,  "D2": 9,  "D3": 10,
    "N1": 9,  "N2": 10, "N3": 11,
}


# ---------------------------------------------------------------------------
# Conversion helpers
# ---------------------------------------------------------------------------

def note_to_midi(note: str) -> int:
    """Convert a western note name (e.g. 'F#') to a MIDI note number."""
    midi = NOTE_TO_MIDI.get(note)
    if midi is None:
        raise ValueError(f"Unknown note name: {note!r}")
    return midi


def swara_to_midi(swara: str, root: int = DEFAULT_ROOT_MIDI) -> int:
    """Convert a Carnatic swara token to a MIDI note number."""
    offset = SWARA_SEMITONES.get(swara)
    if offset is None:
        raise ValueError(f"Unknown swara: {swara!r}")
    return root + offset


# ---------------------------------------------------------------------------
# MIDI file creation
# ---------------------------------------------------------------------------

def create_midi(
    notes: list[str],
    instrument_program: int,
    tempo: int = 90,
) -> str:
    """
    Build a MIDI file from a list of western note names.

    Args:
        notes:              e.g. ["C", "D", "E", "G"]
        instrument_program: GM program number (0-127)
        tempo:              BPM

    Returns:
        Absolute path to the saved .mid file.
    """
    GENERATED_DIR.mkdir(exist_ok=True)

    microseconds_per_beat = mido.bpm2tempo(tempo)
    # ticks for 0.5 s = (TICKS_PER_BEAT * beats_per_second * 0.5)
    beats_per_second = tempo / 60
    ticks_per_note = int(TICKS_PER_BEAT * beats_per_second * 0.5)

    mid = mido.MidiFile(ticks_per_beat=TICKS_PER_BEAT)
    track = mido.MidiTrack()
    mid.tracks.append(track)

    track.append(mido.MetaMessage("set_tempo", tempo=microseconds_per_beat, time=0))
    track.append(mido.Message("program_change", program=instrument_program, channel=0, time=0))

    for note_name in notes:
        midi_note = note_to_midi(note_name)
        track.append(mido.Message("note_on",  note=midi_note, velocity=DEFAULT_VELOCITY, time=0))
        track.append(mido.Message("note_off", note=midi_note, velocity=0, time=ticks_per_note))

    timestamp = int(time.time() * 1000)
    output_path = GENERATED_DIR / f"music_{timestamp}.mid"
    mid.save(str(output_path))

    return str(output_path)


def build_midi_bytes(
    notes: list[int],
    tempo_bpm: int = 80,
    note_duration_beats: float = 0.5,
    velocity: int = DEFAULT_VELOCITY,
    midi_program: int = 40,
) -> bytes:
    """
    Construct a single-track MIDI file from raw MIDI note numbers
    and return the raw bytes (used by the /generate endpoint).
    """
    import io

    microseconds_per_beat = mido.bpm2tempo(tempo_bpm)
    ticks_per_note = int(TICKS_PER_BEAT * note_duration_beats)

    mid = mido.MidiFile(ticks_per_beat=TICKS_PER_BEAT)
    track = mido.MidiTrack()
    mid.tracks.append(track)

    track.append(mido.MetaMessage("set_tempo", tempo=microseconds_per_beat, time=0))
    track.append(mido.Message("program_change", program=midi_program, time=0))

    for note in notes:
        track.append(mido.Message("note_on",  note=note, velocity=velocity, time=0))
        track.append(mido.Message("note_off", note=note, velocity=0, time=ticks_per_note))

    buf = io.BytesIO()
    mid.save(file=buf)
    return buf.getvalue()
