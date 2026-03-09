from pydantic import BaseModel, Field


class GenerateRequest(BaseModel):
    raga: str = Field(..., description="Raga key (e.g. 'mohanam')")
    instrument: str = Field(..., description="Instrument name (e.g. 'veena')")
    tempo: int = Field(default=90, ge=40, le=200, description="Tempo in BPM")
    length: int = Field(default=32, ge=4, le=128, description="Number of notes to generate")


class GenerateResponse(BaseModel):
    raga: str
    instrument: str
    notes: list[str]
    midi_file: str


class RagaResponse(BaseModel):
    id: str
    name: str
    arohanam: list[str]
    avarohanam: list[str]
    vadi: str
    samavadi: str


class InstrumentResponse(BaseModel):
    name: str
    midi_program: int
