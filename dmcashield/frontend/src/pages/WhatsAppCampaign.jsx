import { useState } from 'react';

export default function WhatsAppCampaign() {
  const [connected, setConnected] = useState(false);

  return (
    <div className="main-content animate-in">
      <div className="page-header">
        <h1>💬 WhatsApp Business</h1>
        <p>Connect with leads via WhatsApp</p>
      </div>

      <div className="stats-grid">
        <div className="stat-card green">
          <div className="stat-label">Messages Sent</div>
          <div className="stat-value green">0</div>
        </div>
        <div className="stat-card purple">
          <div className="stat-label">Delivered</div>
          <div className="stat-value purple">0</div>
        </div>
        <div className="stat-card teal">
          <div className="stat-label">Read</div>
          <div className="stat-value teal">0</div>
        </div>
        <div className="stat-card orange">
          <div className="stat-label">Replied</div>
          <div className="stat-value orange">0</div>
        </div>
      </div>

      <div className="glass-card no-hover">
        <h3 style={{ marginBottom: 16 }}>🔗 WhatsApp Connection</h3>
        {connected ? (
          <div>
            <p style={{ color: 'var(--accent-success)', marginBottom: 12 }}>✓ Connected to WhatsApp Business</p>
            <button className="btn btn-danger" onClick={() => setConnected(false)}>Disconnect</button>
          </div>
        ) : (
          <div>
            <div className="form-group">
              <label className="form-label">Phone Number ID</label>
              <input className="form-input" placeholder="Your WhatsApp Phone Number ID" />
            </div>
            <div className="form-group">
              <label className="form-label">Access Token</label>
              <input className="form-input" type="password" placeholder="WhatsApp Business API Token" />
            </div>
            <button className="btn btn-success" onClick={() => setConnected(true)}>Connect WhatsApp</button>
          </div>
        )}
      </div>
    </div>
  );
}