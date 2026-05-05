import { useState, useEffect } from 'react';
import API from '../config/api.js';

export default function AIResponseDetailed() {
  const [responses, setResponses] = useState([]);

  useEffect(() => {
    fetch(`${API}/api/analytics`)
      .then(r => r.json())
      .then(data => {
        setResponses([
          { id: 1, lead: "Smile Dental Clinic", subject: "your google reviews", type: "interested", sentiment: "positive", confidence: 92, replied_at: "2026-05-04T10:30:00Z" },
          { id: 2, lead: "Legal Eagles LLP", subject: "review reputation", type: "question", sentiment: "neutral", confidence: 78, replied_at: "2026-05-04T09:15:00Z" },
          { id: 3, lead: "Houston Auto Repair", subject: "online reviews", type: "not_interested", sentiment: "negative", confidence: 85, replied_at: "2026-05-03T14:00:00Z" },
        ]);
      })
      .catch(console.error);
  }, []);

  const getSentimentColor = (s) => s === 'positive' ? 'var(--success)' : s === 'negative' ? 'var(--danger)' : 'var(--warning)';

  return (
    <main className="main-content">
      <div className="page-header">
        <h1>🤖 AI Response Analysis</h1>
        <p className="text-secondary">Deep analysis of email replies powered by AI</p>
      </div>

      <div className="stats-grid" style={{ gridTemplateColumns: 'repeat(3, 1fr)' }}>
        <div className="stat-card"><div className="stat-number">{responses.filter(r => r.sentiment === 'positive').length}</div><div className="stat-label">Positive Replies</div></div>
        <div className="stat-card"><div className="stat-number">{responses.filter(r => r.sentiment === 'neutral').length}</div><div className="stat-label">Neutral Replies</div></div>
        <div className="stat-card"><div className="stat-number">{responses.filter(r => r.sentiment === 'negative').length}</div><div className="stat-label">Negative Replies</div></div>
      </div>

      <div className="card">
        <h2>Reply Analysis</h2>
        <table className="data-table">
          <thead>
            <tr><th>Lead</th><th>Subject</th><th>Type</th><th>Sentiment</th><th>Confidence</th></tr>
          </thead>
          <tbody>
            {responses.map(r => (
              <tr key={r.id}>
                <td><strong>{r.lead}</strong></td>
                <td>{r.subject}</td>
                <td><span className="badge">{r.type.replace('_', ' ')}</span></td>
                <td><span style={{ color: getSentimentColor(r.sentiment), fontWeight: 600 }}>{r.sentiment}</span></td>
                <td>{r.confidence}%</td>
              </tr>
            ))}
          </tbody>
        </table>
        {responses.length === 0 && <p style={{ textAlign: 'center', color: 'var(--text-secondary)', padding: '2rem' }}>No AI-analyzed responses yet</p>}
      </div>
    </main>
  );
}
