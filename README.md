# Carnatic AI Music Generator

> Demo: generate Carnatic raga-based melodies, play preset tunes in the browser, and download MIDI — FastAPI + React + Tone.js.

[![CI](https://github.com/guptaom31619-prog/Carnatic-AI-Music-Generator/actions/workflows/ci.yml/badge.svg)](https://github.com/guptaom31619-prog/Carnatic-AI-Music-Generator/actions/workflows/ci.yml)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-backend-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB.svg)](https://react.dev/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**Status:** portfolio / demo project — not a production SaaS. Built to show raga-constrained melody generation, MIDI export, and browser playback with Tone.js.

---

## How it works

```
Browser
  └─► React UI  (Vite · Tone.js · :5173)
        └─► FastAPI  (:8000)
              ├─► Raga / instrument / preset APIs
              ├─► Melody generator (raga-constrained notes)
              └─► MIDI writer (mido) → downloadable .mid
```

- Melodies are constrained to the selected Carnatic raga's allowed swaras.
- Presets ship ready-made tunes (national songs, classical phrases, nursery melodies).
- Playback runs entirely in the browser via Tone.js synths (no audio server required).

---

## Features

| Area | What you get |
|------|----------------|
| **Raga generator** | Shankarabharanam, Kalyani, Mohanam, Hamsadhwani |
| **Instruments** | Veena, Violin, Flute, Mridangam, Piano |
| **Controls** | Tempo 60–140 BPM, length 16–64 notes |
| **Presets** | Happy Birthday, Jana Gana Mana, Ode to Joy, and more |
| **Export** | Download generated MIDI files |
| **Playback** | Tone.js synths with per-instrument timbres |

---

## Quick start

### Prerequisites

- Python 3.11+
- Node.js 22+
- `make` (optional but recommended)

### With Make

```bash
git clone https://github.com/guptaom31619-prog/Carnatic-AI-Music-Generator.git
cd Carnatic-AI-Music-Generator

make install
make run
```

| Service | URL |
|---------|-----|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| API docs | http://localhost:8000/docs |

```bash
make test    # pytest + frontend production build
make stop    # stop local servers
make clean   # remove caches, generated MIDI, node_modules
```

### Manual

**Backend**

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend**

```bash
cd frontend
npm install
npm run dev
```

### Docker Compose

```bash
docker compose up --build
```

---

## Project structure

```
Carnatic-AI-Music-Generator/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI routes
│   │   ├── generator.py         # Raga-constrained melody generation
│   │   ├── ragas.py             # Raga definitions + swara mapping
│   │   ├── instruments.py       # Instrument → MIDI program map
│   │   ├── midi_utils.py        # MIDI file construction (mido)
│   │   ├── presets.py           # Built-in preset tunes
│   │   └── models/              # Pydantic request/response schemas
│   ├── tests/                   # pytest suite
│   ├── generated/               # MIDI output (gitignored)
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── App.jsx              # Main UI
│   │   ├── api.js               # API client
│   │   └── components/Player.jsx # Tone.js playback
│   ├── package.json
│   └── Dockerfile
├── .github/workflows/ci.yml     # Backend tests + frontend build
├── docker-compose.yml
├── Makefile
└── LICENSE
```

---

## Environment

No secrets required. Optional overrides:

| Variable | Where | Default | Description |
|----------|-------|---------|-------------|
| `CORS_ORIGINS` | Backend | `http://localhost:5173,http://localhost:3000` | Allowed CORS origins |
| `VITE_API_URL` | Frontend | `http://localhost:8000` | Backend URL (Vite build-time) |

```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

---

## API

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Health check |
| `GET` | `/ragas` | List ragas |
| `GET` | `/instruments` | List instruments |
| `GET` | `/presets` | List presets |
| `GET` | `/presets/{id}` | Preset detail + notes |
| `GET` | `/download/{file}` | Download MIDI |
| `POST` | `/generate` | Generate a composition |

```json
{
  "raga": "Mohanam",
  "instrument": "Violin",
  "tempo": 90,
  "length": 32
}
```

---

## Testing & CI

```bash
make test
```

GitHub Actions runs on every push and PR to `main`:

- **Backend** — Python 3.11, install deps, `pytest`
- **Frontend** — Node 22, `npm ci`, production `vite build`
- **CI Passed** — aggregate gate so the branch status stays green only when both pass

---

## License

MIT — see [LICENSE](LICENSE).
