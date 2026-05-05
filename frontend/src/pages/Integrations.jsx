import { useState, useEffect } from 'react';
import API from '../config/api.js';

export default function Integrations() {
  const [integrations, setIntegrations] = useState({
    slack: { connected: false, channel: '', webhook: '' },
    whatsapp: { connected: false, phone: '', api_url: '' },
    telegram: { connected: false, bot_token: '', chat_id: '' }
  });
  const [testMsg, setTestMsg] = useState('');
  const [sending, setSending] = useState(false);

  const handleConnect = async (type, data) => {
    setIntegrations({ ...integrations, [type]: { ...data, connected: true } });
  };

  const handleDisconnect = (type) => {
    setIntegrations({ ...integrations, [type]: { connected: false } });
  };

  const handleTestMessage = async (type) => {
    if (!testMsg) return;
    setSending(true);
    await fetch(`${API}/api/integrations/${type}/test`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: testMsg })
    });
    setTestMsg('');
    setSending(false);
  };

  return (
    <div className="main-content animate-in">
      <div className="page-header">
        <h1>🔗 Integrations</h1>
        <p>Connect Slack, WhatsApp, Telegram for notifications</p>
      </div>

      {/* Slack */}
      <div className="glass-card no-hover" style={{ marginBottom: 20 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
            <div style={{ fontSize: 32 }}>💬</div>
            <div>
              <h3 style={{ margin: 0 }}>Slack</h3>
              <p style={{ margin: 0, fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Send notifications to Slack channels</p>
            </div>
          </div>
          <span className={`badge ${integrations.slack.connected ? 'badge-active' : 'badge-warm'}`}>
            {integrations.slack.connected ? '✓ Connected' : 'Not Connected'}
          </span>
        </div>
        {integrations.slack.connected ? (
          <div>
            <p style={{ color: 'var(--text-secondary)', marginBottom: 12 }}>📢 Channel: #{integrations.slack.channel}</p>
            <button className="btn btn-danger" onClick={() => handleDisconnect('slack')}>Disconnect</button>
          </div>
        ) : (
          <div className="grid-2">
            <div className="form-group">
              <label className="form-label">Webhook URL</label>
              <input className="form-input" placeholder="https://hooks.slack.com/services/..." 
                onChange={e => setIntegrations({...integrations, slack: { ...integrations.slack, webhook: e.target.value }})} />
            </div>
            <div className="form-group">
              <label className="form-label">Channel Name</label>
              <input className="form-input" placeholder="dmca-alerts" 
                onChange={e => setIntegrations({...integrations, slack: { ...integrations.slack, channel: e.target.value }})} />
            </div>
          </div>
        )}
        {integrations.slack.webflow && (
          <button className="btn btn-primary" onClick={() => handleConnect('slack', integrations.slack)}>
            Connect Slack
          </button>
        )}
      </div>

      {/* WhatsApp */}
      <div className="glass-card no-hover" style={{ marginBottom: 20 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
            <div style={{ fontSize: 32 }}>📱</div>
            <div>
              <h3 style={{ margin: 0 }}>WhatsApp Business</h3>
              <p style={{ margin: 0, fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Send leads via WhatsApp</p>
            </div>
          </div>
          <span className={`badge ${integrations.whatsapp.connected ? 'badge-active' : 'badge-warm'}`}>
            {integrations.whatsapp.connected ? '✓ Connected' : 'Not Connected'}
          </span>
        </div>
        {integrations.whatsapp.connected ? (
          <div>
            <p style={{ color: 'var(--text-secondary)', marginBottom: 12 }}>📞 {integrations.whatsapp.phone}</p>
            <button className="btn btn-danger" onClick={() => handleDisconnect('whatsapp')}>Disconnect</button>
          </div>
        ) : (
          <div className="grid-2">
            <div className="form-group">
              <label className="form-label">WhatsApp API URL</label>
              <input className="form-input" placeholder="https://api.whatsapp.com/..." 
                onChange={e => setIntegrations({...integrations, whatsapp: { ...integrations.whatsapp, api_url: e.target.value }})} />
            </div>
            <div className="form-group">
              <label className="form-label">Phone Number</label>
              <input className="form-input" placeholder="+1234567890" 
                onChange={e => setIntegrations({...integrations, whatsapp: { ...integrations.whatsapp, phone: e.target.value }})} />
            </div>
          </div>
        )}
      </div>

      {/* Telegram */}
      <div className="glass-card no-hover" style={{ marginBottom: 20 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
            <div style={{ fontSize: 32 }}>✈️</div>
            <div>
              <h3 style={{ margin: 0 }}>Telegram</h3>
              <p style={{ margin: 0, fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Get alerts via Telegram bot</p>
            </div>
          </div>
          <span className={`badge ${integrations.telegram.connected ? 'badge-active' : 'badge-warm'}`}>
            {integrations.telegram.connected ? '✓ Connected' : 'Not Connected'}
          </span>
        </div>
        {integrations.telegram.connected ? (
          <div>
            <p style={{ color: 'var(--text-secondary)', marginBottom: 12 }}>🤖 Bot: {integrations.telegram.bot_token?.slice(0, 10)}...</p>
            <button className="btn btn-danger" onClick={() => handleDisconnect('telegram')}>Disconnect</button>
          </div>
        ) : (
          <div className="form-group">
            <label className="form-label">Bot Token</label>
            <input className="form-input" placeholder="123456:ABC-DEF1234ghIkl-zyx57W2vT" 
              onChange={e => setIntegrations({...integrations, telegram: { ...integrations.telegram, bot_token: e.target.value }})} />
          </div>
        )}
        {integrations.telegram.bot_token && (
          <button className="btn btn-primary" onClick={() => handleConnect('telegram', integrations.telegram)}>
            Connect Telegram
          </button>
        )}
      </div>

      {/* Test Message */}
      <div className="glass-card no-hover">
        <h3 style={{ marginBottom: 16 }}>🧪 Test Integration</h3>
        <div className="form-group">
          <label className="form-label">Test Message</label>
          <input className="form-input" placeholder="Your test message..." value={testMsg} onChange={e => setTestMsg(e.target.value)} />
        </div>
        <div style={{ display: 'flex', gap: 8 }}>
          <button className="btn" onClick={() => handleTestMessage('slack')} disabled={sending || !integrations.slack.connected}>
            💬 Test Slack
          </button>
          <button className="btn" onClick={() => handleTestMessage('telegram')} disabled={sending || !integrations.telegram.connected}>
            ✈️ Test Telegram
          </button>
        </div>
      </div>
    </div>
  );
}