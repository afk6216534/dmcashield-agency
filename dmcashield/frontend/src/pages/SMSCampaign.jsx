import { useState, useEffect } from 'react';
const API = 'http://localhost:8000';

export default function SMSCampaign() {
  const [campaigns, setCampaigns] = useState([]);
  const [showNew, setShowNew] = useState(false);
  const [form, setForm] = useState({ name: '', message: '', schedule: '' });

  const handleCreate = async () => {
    const newCampaign = { ...form, id: Date.now(), status: 'draft', sent: 0 };
    setCampaigns([...campaigns, newCampaign]);
    setShowNew(false);
    setForm({ name: '', message: '', schedule: '' });
  };

  return (
    <div className="main-content animate-in">
      <div className="page-header" style={{ display: 'flex', justifyContent: 'space-between' }}>
        <div>
          <h1>📱 SMS Campaigns</h1>
          <p>Send SMS to leads via Twilio or other providers</p>
        </div>
        <button className="btn btn-primary" onClick={() => setShowNew(!showNew)}>
          {showNew ? '✕ Cancel' : '+ New Campaign'}
        </button>
      </div>

      {showNew && (
        <div className="glass-card no-hover" style={{ marginBottom: 20 }}>
          <h3 style={{ marginBottom: 16 }}>📝 New SMS Campaign</h3>
          <div className="form-group">
            <label className="form-label">Campaign Name</label>
            <input className="form-input" placeholder="e.g., Follow-up SMS" value={form.name} onChange={e => setForm({...form, name: e.target.value})} />
          </div>
          <div className="form-group">
            <label className="form-label">Message</label>
            <textarea className="form-input" rows={3} placeholder="Hi {{name}}, following up on our email..." value={form.message} onChange={e => setForm({...form, message: e.target.value})} />
          </div>
          <div className="form-group">
            <label className="form-label">Schedule (optional)</label>
            <input className="form-input" type="datetime-local" value={form.schedule} onChange={e => setForm({...form, schedule: e.target.value})} />
          </div>
          <button className="btn btn-success" onClick={handleCreate}>Create Campaign</button>
        </div>
      )}

      <div className="stats-grid">
        <div className="stat-card purple">
          <div className="stat-label">Total Sent</div>
          <div className="stat-value purple">0</div>
        </div>
        <div className="stat-card teal">
          <div className="stat-label">Delivered</div>
          <div className="stat-value teal">0</div>
        </div>
        <div className="stat-card green">
          <div className="stat-label">Replies</div>
          <div className="stat-value green">0</div>
        </div>
        <div className="stat-card orange">
          <div className="stat-label">Active Campaigns</div>
          <div className="stat-value orange">{campaigns.length}</div>
        </div>
      </div>

      <div className="glass-card no-hover">
        <h3 style={{ marginBottom: 16 }}>📋 Campaign History</h3>
        {campaigns.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon">📱</div>
            <h3>No SMS campaigns yet</h3>
            <p style={{ color: 'var(--text-tertiary)' }}>Create your first SMS campaign</p>
          </div>
        ) : (
          campaigns.map((c, i) => (
            <div key={i} style={{ padding: 16, background: 'var(--bg-tertiary)', borderRadius: 12, marginBottom: 12 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                  <div style={{ fontWeight: 600 }}>{c.name}</div>
                  <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>{c.message?.slice(0, 50)}...</div>
                </div>
                <span className="badge badge-warm">{c.status}</span>
              </div>
            </div>
          ))
        )}
      </div>

      <div className="glass-card no-hover" style={{ marginTop: 20 }}>
        <h3 style={{ marginBottom: 16 }}>⚙️ SMS Provider</h3>
        <div className="form-group">
          <label className="form-label">Provider</label>
          <select className="form-input">
            <option>Twilio (Recommended)</option>
            <option>Nexmo</option>
            <option>AWS SNS</option>
          </select>
        </div>
        <div className="form-group">
          <label className="form-label">API Key / Account SID</label>
          <input className="form-input" placeholder="Your Twilio SID" />
        </div>
        <div className="form-group">
          <label className="form-label">Auth Token</label>
          <input className="form-input" type="password" placeholder="Your Twilio Auth Token" />
        </div>
        <button className="btn btn-primary">Save Provider</button>
      </div>
    </div>
  );
}