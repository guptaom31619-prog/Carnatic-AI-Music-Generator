import { useState, useEffect } from "react";
import {
  getRagas,
  getInstruments,
  getPresets,
  getPresetDetail,
  generateMusic,
  getDownloadUrl,
} from "./api.js";
import Player from "./components/Player.jsx";
import styles from "./App.module.css";

const TABS = { GENERATE: "generate", PRESETS: "presets" };

export default function App() {
  const [ragas, setRagas] = useState([]);
  const [instruments, setInstruments] = useState([]);
  const [presets, setPresets] = useState([]);
  const [activeTab, setActiveTab] = useState(TABS.GENERATE);

  // Generate controls
  const [selectedRaga, setSelectedRaga] = useState("");
  const [selectedInstrument, setSelectedInstrument] = useState("");
  const [tempo, setTempo] = useState(90);
  const [length, setLength] = useState(32);

  // Preset controls
  const [selectedPreset, setSelectedPreset] = useState("");

  // Shared output
  const [generatedMusic, setGeneratedMusic] = useState(null);
  const [playbackNotes, setPlaybackNotes] = useState(null);
  const [playbackTempo, setPlaybackTempo] = useState(90);
  const [playbackInstrument, setPlaybackInstrument] = useState("Piano");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    getRagas().then(setRagas).catch(() => {});
    getInstruments().then(setInstruments).catch(() => {});
    getPresets().then(setPresets).catch(() => {});
  }, []);

  const handleGenerate = async () => {
    if (!selectedRaga || !selectedInstrument) return;
    setLoading(true);
    setError(null);
    try {
      const result = await generateMusic({
        raga: selectedRaga,
        instrument: selectedInstrument,
        tempo,
        length,
      });
      setGeneratedMusic(result);
      setPlaybackNotes(result.notes);
      setPlaybackTempo(tempo);
      setPlaybackInstrument(selectedInstrument);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handlePresetPlay = async (presetId) => {
    setLoading(true);
    setError(null);
    setSelectedPreset(presetId);
    try {
      const detail = await getPresetDetail(presetId);
      setGeneratedMusic(null);
      setPlaybackNotes(detail.notes);
      setPlaybackTempo(detail.tempo);
      setPlaybackInstrument(selectedInstrument || "Piano");
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const canGenerate = selectedRaga && selectedInstrument && !loading;

  // Group presets by category
  const grouped = presets.reduce((acc, p) => {
    (acc[p.category] = acc[p.category] || []).push(p);
    return acc;
  }, {});

  return (
    <div className={styles.layout}>
      {/* ── Hero ── */}
      <header className={styles.hero}>
        <div className={styles.heroGlow} />
        <h1 className={styles.title}>
          Carnatic AI <span className={styles.titleAccent}>Music Generator</span>
        </h1>
        <p className={styles.subtitle}>
          Generate melodies from Carnatic ragas or play classic preset tunes — all in your browser.
        </p>
      </header>

      {/* ── Tabs ── */}
      <nav className={styles.tabs}>
        <button
          className={`${styles.tab} ${activeTab === TABS.GENERATE ? styles.tabActive : ""}`}
          onClick={() => setActiveTab(TABS.GENERATE)}
        >
          Raga Generator
        </button>
        <button
          className={`${styles.tab} ${activeTab === TABS.PRESETS ? styles.tabActive : ""}`}
          onClick={() => setActiveTab(TABS.PRESETS)}
        >
          Preset Tunes
        </button>
      </nav>

      <main className={styles.main}>
        {/* ── GENERATE TAB ── */}
        {activeTab === TABS.GENERATE && (
          <section className={styles.section}>
            <div className={styles.grid2}>
              {/* Raga */}
              <div className={styles.card}>
                <label className={styles.label} htmlFor="raga">Raga</label>
                <select
                  id="raga"
                  className={styles.select}
                  value={selectedRaga}
                  onChange={(e) => setSelectedRaga(e.target.value)}
                >
                  <option value="">Select a raga</option>
                  {ragas.map((r) => (
                    <option key={r} value={r}>{r}</option>
                  ))}
                </select>
              </div>

              {/* Instrument */}
              <div className={styles.card}>
                <label className={styles.label} htmlFor="instrument">Instrument</label>
                <select
                  id="instrument"
                  className={styles.select}
                  value={selectedInstrument}
                  onChange={(e) => setSelectedInstrument(e.target.value)}
                >
                  <option value="">Select an instrument</option>
                  {instruments.map((i) => (
                    <option key={i} value={i}>{i}</option>
                  ))}
                </select>
              </div>
            </div>

            <div className={styles.grid2}>
              {/* Tempo */}
              <div className={styles.card}>
                <label className={styles.label} htmlFor="tempo">
                  Tempo <span className={styles.valueHighlight}>{tempo} BPM</span>
                </label>
                <input
                  id="tempo"
                  type="range"
                  min={60}
                  max={140}
                  step={5}
                  value={tempo}
                  onChange={(e) => setTempo(Number(e.target.value))}
                  className={styles.range}
                />
                <div className={styles.rangeLabels}>
                  <span>Slow</span><span>Fast</span>
                </div>
              </div>

              {/* Length */}
              <div className={styles.card}>
                <label className={styles.label} htmlFor="length">
                  Length <span className={styles.valueHighlight}>{length} notes</span>
                </label>
                <input
                  id="length"
                  type="range"
                  min={16}
                  max={64}
                  step={8}
                  value={length}
                  onChange={(e) => setLength(Number(e.target.value))}
                  className={styles.range}
                />
                <div className={styles.rangeLabels}>
                  <span>Short</span><span>Long</span>
                </div>
              </div>
            </div>

            <button
              className={styles.generateBtn}
              onClick={handleGenerate}
              disabled={!canGenerate}
            >
              {loading ? "Generating…" : "Generate Composition"}
            </button>
          </section>
        )}

        {/* ── PRESETS TAB ── */}
        {activeTab === TABS.PRESETS && (
          <section className={styles.section}>
            {/* Instrument picker for presets */}
            <div className={styles.card}>
              <label className={styles.label} htmlFor="preset-instrument">
                Play presets with
              </label>
              <select
                id="preset-instrument"
                className={styles.select}
                value={selectedInstrument}
                onChange={(e) => setSelectedInstrument(e.target.value)}
              >
                <option value="">Piano (default)</option>
                {instruments.map((i) => (
                  <option key={i} value={i}>{i}</option>
                ))}
              </select>
            </div>

            {Object.entries(grouped).map(([category, items]) => (
              <div key={category} className={styles.presetGroup}>
                <h3 className={styles.presetCategory}>{category}</h3>
                <div className={styles.presetGrid}>
                  {items.map((p) => (
                    <button
                      key={p.id}
                      className={`${styles.presetCard} ${
                        selectedPreset === p.id ? styles.presetActive : ""
                      }`}
                      onClick={() => handlePresetPlay(p.id)}
                      disabled={loading}
                    >
                      <span className={styles.presetName}>{p.name}</span>
                      <span className={styles.presetDesc}>{p.description}</span>
                      <div className={styles.presetMeta}>
                        <span>{p.tempo} BPM</span>
                        <span>{p.note_count} notes</span>
                      </div>
                    </button>
                  ))}
                </div>
              </div>
            ))}
          </section>
        )}

        {/* ── Error ── */}
        {error && <p className={styles.error}>{error}</p>}

        {/* ── Player ── */}
        {playbackNotes && (
          <Player
            midiNotes={playbackNotes}
            tempo={playbackTempo}
            instrument={playbackInstrument}
          />
        )}

        {/* ── Results (only for generated music) ── */}
        {generatedMusic && (
          <div className={styles.resultsCard}>
            <h2 className={styles.resultsTitle}>Generated Composition</h2>

            <div className={styles.resultPills}>
              <span className={styles.resultPill}>{generatedMusic.raga}</span>
              <span className={styles.resultPill}>{generatedMusic.instrument}</span>
              <span className={styles.resultPill}>{tempo} BPM</span>
              <span className={styles.resultPill}>{generatedMusic.notes.length} notes</span>
            </div>

            <div className={styles.notesWrap}>
              <span className={styles.label}>Note Sequence</span>
              <div className={styles.notesGrid}>
                {generatedMusic.notes.map((note, i) => (
                  <span key={i} className={styles.noteChip}>{note}</span>
                ))}
              </div>
            </div>

            <a
              className={styles.downloadBtn}
              href={getDownloadUrl(generatedMusic.midi_file)}
              download
            >
              ↓ Download MIDI
            </a>
          </div>
        )}
      </main>

      <footer className={styles.footer}>
        Carnatic AI Composer &middot; Built with FastAPI + React + Tone.js
      </footer>
    </div>
  );
}
