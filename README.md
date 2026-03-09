# Carnatic AI Music Generator

A full-stack AI-powered Carnatic music composition tool. Generate melodies from Carnatic ragas, play preset tunes (Happy Birthday, Jana Gana Mana, Ode to Joy, and more), and download MIDI files — all in the browser.

---

## Stack

| Layer    | Tech                              |
|----------|-----------------------------------|
| Backend  | Python 3.11+, FastAPI, mido       |
| Frontend | React 18, Vite 5, Tone.js         |
| Testing  | pytest (36 tests), Vite build     |
| CI/CD    | GitHub Actions                    |
| Infra    | Docker Compose (optional)         |

---

## Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── main.py            # FastAPI app + all routes
│   │   ├── generator.py       # Melody generation service
│   │   ├── ragas.py           # Raga definitions + swara mapping
│   │   ├── instruments.py     # Instrument → MIDI program map
│   │   ├── midi_utils.py      # MIDI file construction (mido)
│   │   ├── presets.py         # 10 preset tunes
│   │   └── models/
│   │       └── generation.py  # Pydantic request/response schemas
│   ├── tests/                 # 36 pytest tests
│   ├── generated/             # MIDI output (git-ignored)
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── App.jsx            # Main UI (tabs, controls, results)
│   │   ├── api.js             # API client (env-aware)
│   │   └── components/
│   │       └── Player.jsx     # Tone.js playback with instrument synths
│   ├── index.html
│   ├── vite.config.js
│   ├── package.json
│   ├── Dockerfile
│   └── .env.example
├── .github/workflows/ci.yml   # CI pipeline
├── docker-compose.yml
├── Makefile
└── .gitignore
```

---

## Features

### Raga Generator
- 4 Carnatic ragas: Shankarabharanam, Kalyani, Mohanam, Hamsadhwani
- 5 instruments: Veena, Violin, Flute, Mridangam, Piano
- Adjustable tempo (60–140 BPM) and length (16–64 notes)
- Downloads generated MIDI files

### Preset Tunes
- Happy Birthday, Twinkle Twinkle, Ode to Joy
- Jana Gana Mana, Vande Mataram, Saare Jahan Se Accha
- Raghupati Raghav Raja Ram
- Sa Re Ga Ma Scale, Mohanam Alapana, Kalyani Varnam

### Browser Playback
- Tone.js-powered synthesizer
- Unique synth timbre per instrument (PluckSynth, FMSynth, MembraneSynth, etc.)
- Progress bar and active note highlighting

---

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 20+

### Quick Start (Makefile)

```bash
make install   # Install all dependencies
make run       # Start backend + frontend
```

- Frontend → http://localhost:5173
- Backend  → http://localhost:8000
- API Docs → http://localhost:8000/docs

```bash
make stop      # Stop all servers
make test      # Run all tests
make clean     # Full cleanup
```

### Manual Start

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

### Docker Compose

```bash
docker-compose up --build
```

---

## Environment Variables

No secrets are hardcoded. All configuration is via environment variables with safe defaults.

| Variable       | Where     | Default                                     | Description                       |
|----------------|-----------|---------------------------------------------|-----------------------------------|
| `CORS_ORIGINS` | Backend   | `http://localhost:5173,http://localhost:3000`| Comma-separated allowed origins   |
| `VITE_API_URL` | Frontend  | `http://localhost:8000`                     | Backend API URL (build-time)      |

Copy `.env.example` files to `.env` and adjust for your deployment:

```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

### Deployment Notes

- For **Vercel** (frontend): Set `VITE_API_URL` in the Vercel project environment settings
- For **GCP / AWS / Railway** (backend): Set `CORS_ORIGINS` to your frontend's deployed URL
- No API keys, tokens, or credentials are used in this project

---

## API Endpoints

| Method | Path                | Description                          |
|--------|---------------------|--------------------------------------|
| GET    | `/`                 | Health check                         |
| GET    | `/ragas`            | List available ragas                 |
| GET    | `/instruments`      | List available instruments           |
| GET    | `/presets`          | List all preset tunes                |
| GET    | `/presets/{id}`     | Get preset detail with notes         |
| GET    | `/download/{file}`  | Download a generated MIDI file       |
| POST   | `/generate`         | Generate a MIDI composition          |

**POST /generate** body:
```json
{
  "raga": "Mohanam",
  "instrument": "Violin",
  "tempo": 90,
  "length": 32
}
```

---

## Testing

```bash
make test
```

Runs:
- **Backend**: 36 pytest tests (ragas, instruments, presets, MIDI utils, generator, API routes)
- **Frontend**: Production build check (Vite)

---

## CI/CD

GitHub Actions runs on every push and PR to `main`:
- **Backend job**: Python 3.11, installs deps, runs pytest
- **Frontend job**: Node 20, installs deps, runs production build

---

## Roadmap

- [ ] AI/ML-based phrase generation (Markov chains, RNN)
- [ ] Tala (rhythm cycle) support
- [ ] In-browser MIDI file playback (Web MIDI API)
- [ ] Export to WAV / MP3
- [ ] More ragas and instruments
- [ ] User accounts and saved compositions
