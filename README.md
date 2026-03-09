# Carnatic AI Music Generator

A full-stack AI-powered Carnatic music composition tool.  
Select a raga, instrument, and tempo — generate and download a MIDI composition.

---

## Stack

| Layer    | Tech                          |
|----------|-------------------------------|
| Backend  | Python 3.11, FastAPI, mido    |
| Frontend | React 18, Vite 5              |
| Infra    | Docker Compose                |

---

## Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI app + routes
│   │   ├── generator.py     # Composition orchestration
│   │   ├── ragas.py         # Raga definitions
│   │   ├── instruments.py   # Instrument → MIDI program map
│   │   ├── midi_utils.py    # Swara ↔ MIDI conversion
│   │   └── models/
│   │       └── generation.py  # Pydantic request/response models
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── api.js           # All API calls
│   │   └── components/
│   │       ├── RagaSelector.jsx
│   │       ├── InstrumentSelector.jsx
│   │       ├── Controls.jsx
│   │       └── Player.jsx
│   ├── index.html
│   ├── vite.config.js
│   └── Dockerfile
└── docker-compose.yml
```

---

## Getting Started

### Without Docker

**Backend**
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
# → http://localhost:8000
```

**Frontend**
```bash
cd frontend
npm install
npm run dev
# → http://localhost:5173
```

### With Docker Compose
```bash
docker-compose up --build
```

---

## API Endpoints

| Method | Path          | Description                  |
|--------|---------------|------------------------------|
| GET    | `/`           | Health check                 |
| GET    | `/ragas`      | List available ragas         |
| GET    | `/instruments`| List available instruments   |
| POST   | `/generate`   | Generate a MIDI composition  |

**POST /generate body:**
```json
{
  "raga_id": "bhairavi",
  "instrument_id": "veena",
  "tempo_bpm": 80
}
```

---

## Roadmap

- [ ] AI/ML-based phrase generation
- [ ] In-browser MIDI playback (Web Audio API / Tone.js)
- [ ] Tala (rhythm cycle) support
- [ ] Export to MusicXML / audio
