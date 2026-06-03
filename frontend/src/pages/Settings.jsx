import { useState, useEffect } from 'react';
import API from '../config/api.js';

export default function Settings() {
  const [settings, setSettings] = useState(null);
  const [apiKey, setApiKey] = useState('');
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);

  // Gmail states
  const [gmailEmail, setGmailEmail] = useState('');
  const [gmailPassword, setGmailPassword] = useState('');
  const [gmailDisplayName, setGmailDisplayName] = useState('DMCAShield Agency');
  const [gmailStatus, setGmailStatus] = useState({ status: 'disconnected', email: '' });
  const [gmailTesting, setGmailTesting] = useState(false);
  const [gmailTestResult, setGmailTestResult] = useState(null);
  const [gmailSaving, setGmailSaving] = useState(false);
  const [gmailSaved, setGmailSaved] = useState(false);

  useEffect(() => {
    fetchSettings();
    fetchGmailStatus();
  }, []);

  const fetchSettings = async () => {
    try {
      const res = await fetch(`${API}/api/settings`);
      setSettings(await res.json());
    } catch (err) {
      console.error(err);
    }
  };

  const fetchGmailStatus = async () => {
    try {
      const res = await fetch(`${API}/api/gmail/status`);
      const data = await res.json();
      setGmailStatus(data);
      if (data.email) {
        setGmailEmail(data.email);
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleSaveKey = async () => {
    if (!apiKey.trim()) return;
    setSaving(true);
    await fetch(`${API}/api/settings`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ openrouter_api_key: apiKey }),
    });
    setSaving(false);
    setSaved(true);
    setApiKey('');
    fetchSettings();
    setTimeout(() => setSaved(false), 3000);
  };

  const handleTestGmail = async () => {
    if (!gmailEmail || !gmailPassword) return;
    setGmailTesting(true);
    setGmailTestResult(null);
    try {
      const res = await fetch(`${API}/api/gmail/test`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: gmailEmail, app_password: gmailPassword })
      });
      const data = await res.json();
      setGmailTestResult(data);
    } catch (err) {
      setGmailTestResult({ success: false, message: 'Failed to connect to backend' });
    }
    setGmailTesting(false);
  };

  const handleSaveGmail = async () => {
    if (!gmailEmail || !gmailPassword) return;
    setGmailSaving(true);
    setGmailSaved(false);
    try {
      const res = await fetch(`${API}/api/gmail/configure`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: gmailEmail,
          app_password: gmailPassword,
          display_name: gmailDisplayName || 'DMCAShield Agency'
        })
      });
      const data = await res.json();
      if (data.error) {
        setGmailTestResult({ success: false, message: data.error });
      } else {
        setGmailSaved(true);
        fetchGmailStatus();
        setGmailPassword('');
        setTimeout(() => setGmailSaved(false), 3000);
      }
    } catch (err) {
      setGmailTestResult({ success: false, message: 'Failed to configure Gmail' });
    }
    setGmailSaving(false);
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
              Get a free key at <a href="https://openrouter.ai" target="_blank" rel="noreferrer" style={{ color: 'var(--accent-secondary)' }}>openrouter.ai</a> — powers all AI copywriting, analysis, and sales replies.
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

        {/* Gmail Config Card */}
        <div className="glass-card no-hover" style={{ gridColumn: 'span 2' }}>
          <h3 style={{ marginBottom: 16, fontSize: '1rem', fontWeight: 700 }}>📧 Gmail connection config (Vercel-compatible)</h3>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20 }}>
            <div>
              <div className="form-group">
                <label className="form-label">Gmail Address</label>
                <input className="form-input" type="email" placeholder="your.name@gmail.com" value={gmailEmail} onChange={e => setGmailEmail(e.target.value)} />
              </div>
              <div className="form-group">
                <label className="form-label">Gmail App Password</label>
                <input className="form-input" type="password" placeholder="•••• •••• •••• ••••" value={gmailPassword} onChange={e => setGmailPassword(e.target.value)} />
                <div style={{ fontSize: '0.7rem', color: 'var(--text-tertiary)', marginTop: 4 }}>
                  16-character code from <a href="https://myaccount.google.com/apppasswords" target="_blank" rel="noreferrer" style={{ color: 'var(--accent-secondary)' }}>Google Account Settings</a>. Do NOT use your normal Gmail password.
                </div>
              </div>
              <div className="form-group">
                <label className="form-label">Display Name</label>
                <input className="form-input" type="text" placeholder="DMCAShield Agency" value={gmailDisplayName} onChange={e => setGmailDisplayName(e.target.value)} />
              </div>
              <div style={{ display: 'flex', gap: 10, marginTop: 12 }}>
                <button className="btn btn-secondary" onClick={handleTestGmail} disabled={gmailTesting || !gmailEmail || !gmailPassword}>
                  {gmailTesting ? '⏳ Testing...' : '🔍 Test Connection'}
                </button>
                <button className="btn btn-primary" onClick={handleSaveGmail} disabled={gmailSaving || !gmailEmail || !gmailPassword}>
                  {gmailSaving ? '⏳ Saving...' : '💾 Save & Connect'}
                </button>
              </div>
              {gmailSaved && <div style={{ color: 'var(--accent-success)', fontSize: '0.78rem', marginTop: 8 }}>✅ Gmail credentials verified and saved successfully!</div>}
            </div>

            <div style={{ background: 'var(--bg-tertiary)', padding: 16, borderRadius: 12 }}>
              <h4 style={{ fontWeight: 600, fontSize: '0.9rem', marginBottom: 12 }}>Connection Status</h4>
              <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 16 }}>
                <span className={`status-dot ${gmailStatus?.status === 'connected' ? 'green' : 'red'}`}></span>
                <span style={{ fontSize: '0.85rem', fontWeight: 600 }}>
                  {gmailStatus?.status === 'connected' ? `Connected to ${gmailStatus.email}` : 'Disconnected'}
                </span>
              </div>
              
              {gmailTestResult && (
                <div style={{
                  padding: 12,
                  borderRadius: 8,
                  fontSize: '0.8rem',
                  border: `1px solid ${gmailTestResult.success ? 'rgba(0,184,148,0.3)' : 'rgba(255,107,107,0.3)'}`,
                  background: gmailTestResult.success ? 'rgba(0,184,148,0.06)' : 'rgba(255,107,107,0.06)',
                  color: gmailTestResult.success ? 'var(--accent-success)' : 'var(--accent-hot)'
                }}>
                  <strong>{gmailTestResult.success ? 'Success!' : 'Error:'}</strong> {gmailTestResult.message}
                </div>
              )}

              <div style={{ fontSize: '0.72rem', color: 'var(--text-tertiary)', marginTop: 16, lineHeight: 1.4 }}>
                <p><strong>Note:</strong> On Vercel, the database is ephemeral. Setting these configurations saves them in the local session db. If you configured environment variables on Vercel (`GMAIL_EMAIL` and `GMAIL_APP_PASSWORD`), the system will automatically connect using those credentials even if the SQLite database resets.</p>
              </div>
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
