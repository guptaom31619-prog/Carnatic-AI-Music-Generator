import { useEffect, useRef, useState, useCallback } from "react";
import * as Tone from "tone";
import styles from "./Player.module.css";

// Handle both bare notes ("C" → "C4") and octave-qualified ("C5" stays)
function toToneNote(note) {
  if (/\d$/.test(note)) return note;
  return `${note}4`;
}

// Strip octave for display: "F#4" → "F#"
function displayNote(note) {
  return note.replace(/\d+$/, "");
}

function createSynth(instrument) {
  switch (instrument?.toLowerCase()) {
    case "veena":
      return new Tone.PluckSynth({
        attackNoise: 1.2,
        dampening: 3000,
        resonance: 0.97,
      }).toDestination();

    case "violin":
      return new Tone.FMSynth({
        harmonicity: 3.01,
        modulationIndex: 8,
        oscillator: { type: "sine" },
        envelope: { attack: 0.1, decay: 0.2, sustain: 0.8, release: 1.0 },
        modulation: { type: "triangle" },
        modulationEnvelope: { attack: 0.2, decay: 0.1, sustain: 0.5, release: 0.5 },
      }).toDestination();

    case "flute":
      return new Tone.Synth({
        oscillator: { type: "sine" },
        envelope: { attack: 0.15, decay: 0.05, sustain: 0.9, release: 0.6 },
      }).toDestination();

    case "mridangam":
      return new Tone.MembraneSynth({
        pitchDecay: 0.05,
        octaves: 4,
        oscillator: { type: "sine" },
        envelope: { attack: 0.001, decay: 0.3, sustain: 0, release: 0.3 },
      }).toDestination();

    case "piano":
    default:
      return new Tone.PolySynth(Tone.Synth, {
        oscillator: { type: "triangle" },
        envelope: { attack: 0.005, decay: 0.3, sustain: 0.2, release: 0.8 },
      }).toDestination();
  }
}

export default function Player({ midiNotes, tempo, instrument }) {
  const synthRef = useRef(null);
  const eventsRef = useRef([]);
  const [isPlaying, setIsPlaying] = useState(false);
  const [activeIndex, setActiveIndex] = useState(null);
  const [progress, setProgress] = useState(0);

  const stopPlayback = useCallback(() => {
    Tone.getTransport().stop();
    Tone.getTransport().cancel();
    eventsRef.current = [];
    if (synthRef.current) {
      synthRef.current.dispose();
      synthRef.current = null;
    }
    setIsPlaying(false);
    setActiveIndex(null);
    setProgress(0);
  }, []);

  useEffect(() => {
    stopPlayback();
    return () => stopPlayback();
  }, [midiNotes, tempo, instrument, stopPlayback]);

  async function handlePlay() {
    await Tone.start();
    stopPlayback();

    const synth = createSynth(instrument);
    synthRef.current = synth;

    const secondsPerNote = 60 / tempo / 2;
    const noteDuration = secondsPerNote * 0.85;

    midiNotes.forEach((note, i) => {
      const startTime = i * secondsPerNote;
      const toneNote = toToneNote(note);

      const event = new Tone.ToneEvent((time) => {
        synth.triggerAttackRelease(toneNote, noteDuration, time);
        Tone.getDraw().schedule(() => {
          setActiveIndex(i);
          setProgress(((i + 1) / midiNotes.length) * 100);
        }, time);
      });
      event.start(startTime);
      eventsRef.current.push(event);
    });

    const totalDuration = midiNotes.length * secondsPerNote;
    const endEvent = new Tone.ToneEvent(() => {
      Tone.getDraw().schedule(() => {
        setIsPlaying(false);
        setActiveIndex(null);
        setProgress(100);
      }, Tone.now());
      Tone.getTransport().stop();
    });
    endEvent.start(totalDuration);
    eventsRef.current.push(endEvent);

    Tone.getTransport().start();
    setIsPlaying(true);
  }

  return (
    <div className={styles.card}>
      <div className={styles.topRow}>
        <div className={styles.meta}>
          <span className={styles.title}>Now Playing</span>
          {instrument && (
            <span className={styles.instrumentBadge}>{instrument}</span>
          )}
          <span className={styles.tempoInfo}>{tempo} BPM</span>
        </div>
        <div className={styles.controls}>
          <button
            className={`${styles.btn} ${styles.play}`}
            onClick={handlePlay}
            disabled={isPlaying}
          >
            {isPlaying ? "♪ Playing…" : "▶ Play"}
          </button>
          <button
            className={`${styles.btn} ${styles.stop}`}
            onClick={stopPlayback}
            disabled={!isPlaying}
          >
            ■ Stop
          </button>
        </div>
      </div>

      {/* Progress bar */}
      <div className={styles.progressTrack}>
        <div
          className={styles.progressBar}
          style={{ width: `${progress}%` }}
        />
      </div>

      {/* Note strip */}
      <div className={styles.noteStrip}>
        {midiNotes.map((note, i) => (
          <span
            key={i}
            className={`${styles.notePill} ${
              i === activeIndex ? styles.active : ""
            } ${activeIndex !== null && i < activeIndex ? styles.played : ""}`}
          >
            {displayNote(note)}
          </span>
        ))}
      </div>
    </div>
  );
}
