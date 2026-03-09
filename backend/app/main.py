from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from app.generator import generate_composition, GenerationError
from app.ragas import get_all_ragas
from app.instruments import get_all_instruments
from app.presets import get_all_presets, get_preset
from app.models.generation import GenerateRequest, GenerateResponse

GENERATED_DIR = Path(__file__).resolve().parent.parent / "generated"

app = FastAPI(title="Carnatic AI Composer API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Carnatic AI Composer API running"}


@app.get("/ragas", response_model=list[str])
def list_ragas():
    return [r["name"] for r in get_all_ragas()]


@app.get("/instruments", response_model=list[str])
def list_instruments():
    return [name.capitalize() for name in get_all_instruments()]


@app.get("/presets")
def list_presets():
    return get_all_presets()


@app.get("/presets/{preset_id}")
def get_preset_detail(preset_id: str):
    preset = get_preset(preset_id)
    if preset is None:
        raise HTTPException(status_code=404, detail="Preset not found")
    return preset


@app.get("/download/{filename}")
def download(filename: str):
    file_path = GENERATED_DIR / filename
    if not file_path.exists() or file_path.suffix != ".mid":
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(
        path=str(file_path),
        media_type="audio/midi",
        filename=filename,
    )


@app.post("/generate", response_model=GenerateResponse)
def generate(request: GenerateRequest):
    try:
        return generate_composition(
            raga_name=request.raga,
            instrument_name=request.instrument,
            tempo=request.tempo,
            length=request.length,
        )
    except GenerationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
