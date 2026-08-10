import { useState } from 'react';
import './App.css';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

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

  return (
    <div
      className="app"
      style={{ backgroundColor: result?.theme_color || '#111', minHeight: '100vh', color: '#fff', padding: '2rem' }}
    >
      <h1>Mood Mirror</h1>
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Type how you're feeling..."
        rows={4}
        style={{ width: '100%', maxWidth: '500px', display: 'block', margin: '1rem 0' }}
      />
      <button onClick={handleAnalyze} disabled={loading}>
        {loading ? 'Analyzing...' : 'Reveal My Character'}
      </button>

      {error && <p className="error" style={{ color: 'red' }}>{error}</p>}

      {result && !isMixed && (
        <div className="result" style={{ marginTop: '2rem', background: 'rgba(0,0,0,0.5)', padding: '1rem', borderRadius: '8px' }}>
          <h2>{result.character}</h2>
          <p className="tagline">"{result.tagline}"</p>
          <p className="emotion">
            Dominant emotion: <strong>{result.dominant_emotion}</strong> (
            {(result.confidence * 100).toFixed(0)}%)
          </p>
        </div>
      )}

      {result && isMixed && (
        <div className="result mixed" style={{ marginTop: '2rem', background: 'rgba(0,0,0,0.5)', padding: '1rem', borderRadius: '8px' }}>
          <h2>Mixed feelings detected</h2>
          <p>Your text doesn't clearly point to one character — here are the top two matches:</p>
          <div style={{ display: 'flex', gap: '1rem', marginTop: '1rem', flexWrap: 'wrap' }}>
            {result.candidates.map((c) => (
              <div
                key={c.emotion}
                style={{
                  flex: '1 1 200px',
                  background: c.theme_color,
                  padding: '1rem',
                  borderRadius: '8px',
                }}
              >
                <h3 style={{ margin: 0 }}>{c.character}</h3>
                <p style={{ margin: '0.25rem 0 0' }}>
                  {c.emotion} ({(c.confidence * 100).toFixed(0)}%)
                </p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;