import { useState } from 'react';
import './App.css';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Maps backend `matched_emotion` values to theme class + accent color.
// Character NAMES still come from the backend (character_mapper.py) —
// this just controls which visual theme wraps the result.
const THEME_CONFIG = {
  joy: { themeClass: 'theme-joy', accent: '#C41E3A' },
  sadness: { themeClass: 'theme-sadness', accent: '#6B7280' },
  anger: { themeClass: 'theme-anger', accent: '#3CB043' },
  fear: { themeClass: 'theme-fear', accent: '#8B0000' },
  surprise: { themeClass: 'theme-surprise', accent: '#FFC72C' },
  disgust: { themeClass: 'theme-disgust', accent: '#D4AF37' },
  neutral: { themeClass: 'theme-neutral', accent: '#1E4FA0' },
};

/* ---------- Original motif icons (one per emotion, not character likenesses) ---------- */

function WebMotif({ color }) {
  // Joy — diagonal web-lines, radiating energy
  return (
    <svg className="motif-icon" viewBox="0 0 200 200" fill="none">
      <g stroke={color} strokeWidth="2" opacity="0.9">
        {[0, 30, 60, 90, 120, 150].map((deg) => (
          <line
            key={deg}
            x1="100"
            y1="100"
            x2={100 + 90 * Math.cos((deg * Math.PI) / 180)}
            y2={100 + 90 * Math.sin((deg * Math.PI) / 180)}
          />
        ))}
        {[25, 50, 75].map((r) => (
          <circle key={r} cx="100" cy="100" r={r} opacity="0.6" />
        ))}
      </g>
    </svg>
  );
}

function WingMotif({ color }) {
  // Sadness — twin wing silhouettes, folded inward
  return (
    <svg className="motif-icon" viewBox="0 0 200 200" fill="none">
      <path
        d="M100 60 C60 40 20 55 10 90 C40 80 65 85 90 105 C70 95 45 100 25 115 C55 110 80 118 100 140"
        stroke={color}
        strokeWidth="3"
        fill="none"
      />
      <path
        d="M100 60 C140 40 180 55 190 90 C160 80 135 85 110 105 C130 95 155 100 175 115 C145 110 120 118 100 140"
        stroke={color}
        strokeWidth="3"
        fill="none"
      />
    </svg>
  );
}

function ImpactMotif({ color }) {
  // Anger — cracked impact burst
  return (
    <svg className="motif-icon" viewBox="0 0 200 200" fill="none">
      <circle cx="100" cy="100" r="70" stroke={color} strokeWidth="3" opacity="0.4" />
      {[0, 45, 90, 135, 180, 225, 270, 315].map((deg) => (
        <line
          key={deg}
          x1={100 + 30 * Math.cos((deg * Math.PI) / 180)}
          y1={100 + 30 * Math.sin((deg * Math.PI) / 180)}
          x2={100 + 85 * Math.cos((deg * Math.PI) / 180)}
          y2={100 + 85 * Math.sin((deg * Math.PI) / 180)}
          stroke={color}
          strokeWidth="4"
        />
      ))}
      <circle cx="100" cy="100" r="18" fill={color} opacity="0.85" />
    </svg>
  );
}

function RadarMotif({ color }) {
  // Fear — sonar/heightened-sense arcs
  return (
    <svg className="motif-icon" viewBox="0 0 200 200" fill="none">
      <g stroke={color} strokeWidth="2.5">
        <path d="M40 140 A85 85 0 0 1 160 140" opacity="0.9" />
        <path d="M60 140 A60 60 0 0 1 140 140" opacity="0.65" />
        <path d="M80 140 A35 35 0 0 1 120 140" opacity="0.4" />
      </g>
      <circle cx="100" cy="140" r="6" fill={color} />
    </svg>
  );
}

function LightningMotif({ color }) {
  // Surprise — speed streak / lightning
  return (
    <svg className="motif-icon" viewBox="0 0 200 200" fill="none">
      <path
        d="M110 20 L60 105 L95 105 L80 180 L145 90 L108 90 Z"
        fill={color}
        opacity="0.9"
      />
      <line x1="20" y1="60" x2="55" y2="60" stroke={color} strokeWidth="3" opacity="0.5" />
      <line x1="15" y1="90" x2="50" y2="90" stroke={color} strokeWidth="3" opacity="0.35" />
    </svg>
  );
}

function ClawMotif({ color }) {
  // Disgust — claw-slash marks
  return (
    <svg className="motif-icon" viewBox="0 0 200 200" fill="none">
      <g stroke={color} strokeWidth="6" strokeLinecap="round" opacity="0.9">
        <line x1="40" y1="30" x2="100" y2="170" />
        <line x1="70" y1="25" x2="130" y2="165" />
        <line x1="100" y1="20" x2="160" y2="160" />
      </g>
    </svg>
  );
}

function CalmMotif({ color }) {
  // Neutral — steady radial glow, balanced rings
  return (
    <svg className="motif-icon" viewBox="0 0 200 200" fill="none">
      <circle cx="100" cy="100" r="80" stroke={color} strokeWidth="2" opacity="0.3" />
      <circle cx="100" cy="100" r="55" stroke={color} strokeWidth="2.5" opacity="0.55" />
      <circle cx="100" cy="100" r="28" fill={color} opacity="0.85" />
    </svg>
  );
}

const MOTIFS = {
  joy: WebMotif,
  sadness: WingMotif,
  anger: ImpactMotif,
  fear: RadarMotif,
  surprise: LightningMotif,
  disgust: ClawMotif,
  neutral: CalmMotif,
};

function App() {
  const [text, setText] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleAnalyze = async () => {
    if (!text.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_URL}/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text }),
      });
      if (!res.ok) throw new Error('Request failed');
      const data = await res.json();
      setResult(data);
    } catch (err) {
      setError('Something went wrong. Try again.');
    } finally {
      setLoading(false);
    }
  };

  const isMixed = result?.status === 'mixed';
  const dominant = result?.matched_emotion;
  const theme = THEME_CONFIG[dominant];
  const themeClass = theme?.themeClass || 'theme-default';
  const Motif = MOTIFS[dominant];

  return (
    <div className={`app ${themeClass}`}>
      <div className="header">
        <h1 className="logo-main">MOOD</h1>
        <span className="logo-sub">MIRROR</span>
      </div>

      <div className="prompt-row">
        <input
          className="prompt-input"
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Type how you're feeling..."
          onKeyDown={(e) => e.key === 'Enter' && handleAnalyze()}
        />
        <button className="enter-btn" onClick={handleAnalyze} disabled={loading}>
          {loading ? '...' : 'Enter'}
        </button>
      </div>

      {error && <p className="status-text error-text">{error}</p>}

      {!result && !error && (
        <div className="empty-state">
          <p>Write a sentence about how you're feeling right now — Mood Mirror will read the emotion and show you the character it matches.</p>
        </div>
      )}

      {result && !isMixed && (
        <div className="result-row">
          {Motif && <Motif color={theme.accent} />}
          <div className="character-info">
            <h2>{result.character}</h2>
            <p className="emotion">{result.matched_emotion} · {result.matched_theme}</p>
            <p className="confidence">Confidence {(result.confidence * 100).toFixed(0)}%</p>
          </div>
        </div>
      )}

      {result && isMixed && (
        <div className="mixed-row">
          <h2 className="mixed-heading">Mixed feelings detected</h2>
          <p className="mixed-subtext">Your text doesn't clearly point to one character — top matches:</p>
          <div className="candidate-cards">
            {result.candidates.map((c, i) => (
              <div className="candidate-card" key={i} style={{ borderColor: c.theme_color }}>
                <h3>{c.character}</h3>
                <p>{(c.confidence * 100).toFixed(0)}% match</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;