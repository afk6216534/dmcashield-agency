import { useState } from 'react';

export default function ColdCalling() {
  const [calling, setCalling] = useState(false);

  return (
    <div className="main-content animate-in">
      <div className="page-header">
        <h1>📞 Cold Calling</h1>
        <p>AI-powered voice calls to leads</p>
      </div>

      <div className="stats-grid">
        <div className="stat-card green">
          <div className="stat-label">Calls Made</div>
          <div className="stat-value green">0</div>
        </div>
        <div className="stat-card teal">
          <div className="stat-label">Connected</div>
          <div className="stat-value teal">0</div>
        </div>
        <div className="stat-card purple">
          <div className="stat-label">Qualified</div>
          <div className="stat-value purple">0</div>
        </div>
        <div className="stat-card orange">
          <div className="stat-label">Appointments</div>
          <div className="stat-value orange">0</div>
        </div>
      </div>

      <div className="glass-card no-hover">
        <h3 style={{ marginBottom: 16 }}>🎙️ Voice Provider</h3>
        <div className="form-group">
          <label className="form-label">Provider</label>
          <select className="form-input">
            <option>ElevenLabs (AI Voice)</option>
            <option>Twilio Voice</option>
            <option>Google Cloud TTS</option>
          </select>
        </div>
        <div className="form-group">
          <label className="form-label">Voice ID</label>
          <input className="form-input" placeholder="Voice ID from provider" />
        </div>
        <button className="btn btn-primary">Save Settings</button>
      </div>

      <div className="glass-card no-hover" style={{ marginTop: 20 }}>
        <h3 style={{ marginBottom: 16 }}>📝 Call Script</h3>
        <div className="form-group">
          <label className="form-label">Opening Script</label>
          <textarea className="form-input" rows={4} placeholder="Hi, this is {{agent_name}} from {{company}}..." />
        </div>
        <div className="form-group">
          <label className="form-label">Qualifying Questions</label>
          <textarea className="form-input" rows={4} placeholder="Are you interested in..." />
        </div>
        <button className="btn btn-success">Save Script</button>
      </div>

      <div className="glass-card no-hover" style={{ marginTop: 20 }}>
        <h3 style={{ marginBottom: 16 }}>▶️ Start Campaign</h3>
        <div style={{ display: 'flex', gap: 12 }}>
          <button className="btn btn-primary" onClick={() => setCalling(true)}>Start Calling</button>
          <button className="btn btn-danger" onClick={() => setCalling(false)}>Stop</button>
        </div>
        {calling && <p style={{ marginTop: 12, color: 'var(--accent-success)' }}>Calling in progress...</p>}
      </div>
    </div>
  );
}