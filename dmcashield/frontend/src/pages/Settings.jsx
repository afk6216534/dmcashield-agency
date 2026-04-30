import { useState, useEffect } from 'react';
const API = 'http://localhost:8000';

export default function Settings() {
  const [settings, setSettings] = useState(null);
  const [apiKey, setApiKey] = useState('');
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);

  useEffect(() => { fetch(`${API}/api/settings`).then(r => r.json()).then(setSettings).catch(console.error); }, []);

  const handleSaveKey = async () => {
    if (!apiKey.trim()) return;
    setSaving(true);
    await fetch(`${API}/api/settings`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ openrouter_api_key: apiKey }),
    });
    setSaving(false);
    setSaved(true);
    setApiKey('');
    setTimeout(() => setSaved(false), 3000);
  };

  return (
    <div className="main-content animate-in">
      <div className="page-header">
        <h1>⚙️ Settings</h1>
        <p>Configure your DMCAShield Agency system</p>
      </div>

      <div className="grid-2">
        <div className="glass-card no-hover">
          <h3 style={{ marginBottom: 16, fontSize: '1rem', fontWeight: 700 }}>🔑 API Configuration</h3>
          <div className="form-group">
            <label className="form-label">OpenRouter API Key</label>
            <div style={{ display: 'flex', gap: 8 }}>
              <input className="form-input" type="password" placeholder={settings?.openrouter_configured ? '••••••••••••• (configured)' : 'sk-or-...'} value={apiKey} onChange={e => setApiKey(e.target.value)} />
              <button className="btn btn-primary" onClick={handleSaveKey} disabled={saving}>{saving ? '...' : '💾'}</button>
            </div>
            {saved && <div style={{ color: 'var(--accent-success)', fontSize: '0.78rem', marginTop: 6 }}>✅ API key saved!</div>}
            <div style={{ fontSize: '0.72rem', color: 'var(--text-tertiary)', marginTop: 6 }}>
              Get a free key at <a href="https://openrouter.ai" target="_blank" style={{ color: 'var(--accent-secondary)' }}>openrouter.ai</a> — powers all AI copywriting, analysis, and sales replies.
            </div>
          </div>

          <div style={{ marginTop: 20 }}>
            <div className="form-label">Status</div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              <span className={`status-dot ${settings?.openrouter_configured ? 'green' : 'red'}`}></span>
              <span style={{ fontSize: '0.82rem' }}>{settings?.openrouter_configured ? 'OpenRouter Connected' : 'Not configured — AI features disabled'}</span>
            </div>
          </div>
        </div>

        <div className="glass-card no-hover">
          <h3 style={{ marginBottom: 16, fontSize: '1rem', fontWeight: 700 }}>📤 Email Sending Limits</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
            <div>
              <span style={{ fontSize: '0.78rem', color: 'var(--text-secondary)' }}>Max emails per account per day:</span>
              <div style={{ fontWeight: 700, fontSize: '1.2rem' }}>{settings?.max_emails_per_day || 40}</div>
            </div>
            <div>
              <span style={{ fontSize: '0.78rem', color: 'var(--text-secondary)' }}>Gap between sends:</span>
              <div style={{ fontWeight: 700, fontSize: '1.2rem' }}>{Math.floor((settings?.email_gap_min || 180) / 60)}–{Math.floor((settings?.email_gap_max || 420) / 60)} minutes</div>
            </div>
          </div>
        </div>

        <div className="glass-card no-hover">
          <h3 style={{ marginBottom: 16, fontSize: '1rem', fontWeight: 700 }}>🤖 AI Models</h3>
          {settings?.models && Object.entries(settings.models).map(([role, model]) => (
            <div key={role} style={{ padding: '8px 0', borderBottom: '1px solid var(--border-subtle)', display: 'flex', justifyContent: 'space-between' }}>
              <span style={{ fontSize: '0.82rem', fontWeight: 600, textTransform: 'capitalize' }}>{role}</span>
              <span style={{ fontSize: '0.72rem', color: 'var(--accent-secondary)', fontFamily: 'var(--font-mono)' }}>{model}</span>
            </div>
          ))}
        </div>

        <div className="glass-card no-hover">
          <h3 style={{ marginBottom: 16, fontSize: '1rem', fontWeight: 700 }}>💡 System Info</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 8, fontSize: '0.82rem' }}>
            <div><span style={{ color: 'var(--text-tertiary)' }}>Backend:</span> FastAPI + Python</div>
            <div><span style={{ color: 'var(--text-tertiary)' }}>Frontend:</span> React + Vite</div>
            <div><span style={{ color: 'var(--text-tertiary)' }}>Database:</span> SQLite (local)</div>
            <div><span style={{ color: 'var(--text-tertiary)' }}>Memory:</span> ChromaDB (local vectors)</div>
            <div><span style={{ color: 'var(--text-tertiary)' }}>Agents:</span> 12 departments, 50+ agents</div>
          </div>
        </div>
      </div>
    </div>
  );
}
