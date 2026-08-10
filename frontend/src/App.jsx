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

      {result && (
        <div className="result" style={{ marginTop: '2rem', background: 'rgba(0,0,0,0.5)', padding: '1rem', borderRadius: '8px' }}>
          <h2>{result.character}</h2>
          <p className="tagline">"{result.tagline}"</p>
          <p className="emotion">
            Dominant emotion: <strong>{result.dominant_emotion}</strong> (
            {(result.confidence * 100).toFixed(0)}%)
          </p>
        </div>
      )}
    </div>
  );
}

export default App;