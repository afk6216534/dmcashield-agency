import { useState } from 'react';

export default function LinkedInOutreach() {
  const [connected, setConnected] = useState(false);

  return (
    <div className="main-content animate-in">
      <div className="page-header">
        <h1>💼 LinkedIn Outreach</h1>
        <p>Automated LinkedIn connection requests and messaging</p>
      </div>

      <div className="stats-grid">
        <div className="stat-card blue">
          <div className="stat-label">Connections Sent</div>
          <div className="stat-value blue">0</div>
        </div>
        <div className="stat-card purple">
          <div className="stat-label">Accepted</div>
          <div className="stat-value purple">0</div>
        </div>
        <div className="stat-card green">
          <div className="stat-label">Messages Sent</div>
          <div className="stat-value green">0</div>
        </div>
        <div className="stat-card orange">
          <div className="stat-label">Responses</div>
          <div className="stat-value orange">0</div>
        </div>
      </div>

      <div className="glass-card no-hover">
        <h3 style={{ marginBottom: 16 }}>🔗 LinkedIn Account</h3>
        {connected ? (
          <div>
            <p style={{ color: 'var(--accent-success)', marginBottom: 12 }}>✓ Connected</p>
            <button className="btn btn-danger" onClick={() => setConnected(false)}>Disconnect</button>
          </div>
        ) : (
          <div>
            <div className="form-group">
              <label className="form-label">Email / Phone</label>
              <input className="form-input" placeholder="Your LinkedIn email" />
            </div>
            <div className="form-group">
              <label className="form-label">Password</label>
              <input className="form-input" type="password" placeholder="Your LinkedIn password" />
            </div>
            <button className="btn btn-primary" onClick={() => setConnected(true)}>Connect LinkedIn</button>
          </div>
        )}
      </div>

      <div className="glass-card no-hover" style={{ marginTop: 20 }}>
        <h3 style={{ marginBottom: 16 }}>📝 Outreach Templates</h3>
        <div className="form-group">
          <label className="form-label">Connection Request Template</label>
          <textarea className="form-input" rows={3} placeholder="Hi {{name}}, I'd love to connect..." />
        </div>
        <div className="form-group">
          <label className="form-label">Follow-up Template</label>
          <textarea className="form-input" rows={3} placeholder="Hi {{name}}, just following up..." />
        </div>
        <button className="btn btn-success">Save Templates</button>
      </div>
    </div>
  );
}