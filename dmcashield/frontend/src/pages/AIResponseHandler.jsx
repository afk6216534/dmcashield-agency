import { useState, useEffect } from 'react';
const API = 'http://localhost:8000';

export default function AIResponseHandler() {
  const [rules, setRules] = useState([]);
  const [responses, setResponses] = useState([]);
  const [enabled, setEnabled] = useState(true);

  const defaultRules = [
    { trigger: 'interested', response: 'Great! Let me schedule a call with you.', category: 'positive' },
    { trigger: 'not interested', response: 'No problem. We appreciate your time!', category: 'negative' },
    { trigger: 'pricing', response: 'Our plans start at $97/mo. Would you like details?', category: 'question' },
    { trigger: 'call me', response: 'Sure! What time works best for you?', category: 'question' },
  ];

  useEffect(() => { setRules(defaultRules); }, []);

  const handleSave = async (rule) => {
    // Save to backend
  };

  return (
    <div className="main-content animate-in">
      <div className="page-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <div>
          <h1>🤖 AI Response Handler</h1>
          <p>Auto-respond to email replies with AI</p>
        </div>
        <label style={{ display: 'flex', alignItems: 'center', gap: 10, cursor: 'pointer', background: 'var(--bg-tertiary)', padding: '10px 16px', borderRadius: 10 }}>
          <input type="checkbox" checked={enabled} onChange={e => setEnabled(e.target.checked)} />
          <span style={{ fontWeight: 600, color: enabled ? 'var(--accent-success)' : 'var(--text-tertiary)' }}>
            {enabled ? '✓ Active' : 'Paused'}
          </span>
        </label>
      </div>

      {/* Stats */}
      <div className="stats-grid">
        <div className="stat-card green"><div className="stat-label">Replies Processed</div><div className="stat-value green">142</div></div>
        <div className="stat-card purple"><div className="stat-label">Auto-Responded</div><div className="stat-value purple">128</div></div>
        <div className="stat-card teal"><div className="stat-label">Avg Response Time</div><div className="stat-value teal">2s</div></div>
        <div className="stat-card orange"><div className="stat-label">Success Rate</div><div className="stat-value orange">94%</div></div>
      </div>

      {/* Response Rules */}
      <div className="glass-card no-hover">
        <h3 style={{ marginBottom: 16 }}>📋 Response Rules</h3>
        {rules.map((rule, i) => (
          <div key={i} style={{ padding: '12px 0', borderBottom: '1px solid var(--border-subtle)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div>
              <span className="badge" style={{ background: rule.category === 'positive' ? 'var(--accent-success)' : rule.category === 'negative' ? 'var(--accent-hot)' : 'var(--accent-primary)', marginRight: 8 }}>
                {rule.trigger}
              </span>
            </div>
            <div style={{ flex: 1, color: 'var(--text-secondary)', fontSize: '0.86rem' }}>{rule.response}</div>
            <button className="btn" style={{ padding: '4px 10px', fontSize: '0.72rem' }}>Edit</button>
          </div>
        ))}
      </div>

      {/* Quick Add */}
      <div className="glass-card no-hover" style={{ marginTop: 20 }}>
        <h3 style={{ marginBottom: 16 }}>➕ Add New Rule</h3>
        <div className="grid-2">
          <div className="form-group">
            <label className="form-label">Trigger Keyword</label>
            <input className="form-input" placeholder="e.g., pricing, demo, call" />
          </div>
          <div className="form-group">
            <label className="form-label">Category</label>
            <select className="form-input">
              <option>Positive</option>
              <option>Negative</option>
              <option>Question</option>
            </select>
          </div>
        </div>
        <div className="form-group">
          <label className="form-label">Auto Response</label>
          <textarea className="form-input" rows={3} placeholder="Thank you for your interest..." />
        </div>
        <button className="btn btn-primary">+ Add Rule</button>
      </div>
    </div>
  );
}