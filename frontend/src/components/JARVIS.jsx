import { useState } from 'react';
import { useLocation } from 'react-router-dom';
import API from '../config/api.js';

export default function JARVIS() {
  const [input, setInput] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);
  const location = useLocation();

  // Hide bottom bar on the full JARVIS chat page to avoid duplicate
  if (location.pathname === '/jarvis') return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;
    setLoading(true);
    try {
      const res = await fetch(`${API}/api/jarvis/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input }),
      });
      const data = await res.json();
      setResponse(data.response || 'No response');
    } catch (err) {
      setResponse('Connection error — is the backend running?');
    }
    setLoading(false);
    setInput('');
  };

  return (
    <div className="jarvis-bar">
      <span className="jarvis-label">JARVIS ›</span>
      <form onSubmit={handleSubmit} style={{ flex: 1, display: 'flex', gap: 12 }}>
        <input
          className="jarvis-input"
          type="text"
          placeholder={response || "Ask JARVIS anything... (e.g., 'How many hot leads?')"}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          disabled={loading}
        />
        <button className="btn btn-primary" type="submit" disabled={loading} style={{ borderRadius: 20 }}>
          {loading ? '...' : '⚡'}
        </button>
      </form>
    </div>
  );
}
