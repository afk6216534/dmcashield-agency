import { useState, useEffect } from 'react';
import API from '../config/api.js';

export default function EmailAccounts() {
  const [accounts, setAccounts] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [provider, setProvider] = useState('gmail');
  const [form, setForm] = useState({ email_address: '', display_name: '', app_password: '' });
  const [adding, setAdding] = useState(false);

  // V5.0 Real Gmail Connection State
  const [gmailStatus, setGmailStatus] = useState({ status: 'disconnected', email: '', display_name: '' });
  const [gmailForm, setGmailForm] = useState({ email: '', app_password: '', display_name: 'DMCAShield Agency' });
  const [testingGmail, setTestingGmail] = useState(false);
  const [gmailError, setGmailError] = useState('');
  const [gmailSuccess, setGmailSuccess] = useState('');

  useEffect(() => { 
    fetchAccounts(); 
    fetchGmailStatus();
  }, []);

  const fetchGmailStatus = async () => {
    try {
      const res = await fetch(`${API}/api/gmail/status`);
      const data = await res.json();
      setGmailStatus(data);
      if (data.email) {
        setGmailForm(prev => ({ ...prev, email: data.email, display_name: data.display_name || prev.display_name }));
      }
    } catch (err) {
      console.error('Failed to fetch Gmail status:', err);
    }
  };

  const handleTestGmail = async () => {
    setTestingGmail(true);
    setGmailError('');
    setGmailSuccess('');
    try {
      const res = await fetch(`${API}/api/gmail/test`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: gmailForm.email, app_password: gmailForm.app_password }),
      });
      const data = await res.json();
      if (data.success) {
        setGmailSuccess('✅ SMTP Connection verified successfully!');
      } else {
        setGmailError(`❌ SMTP Connection failed: ${data.message}`);
      }
    } catch (err) {
      setGmailError('❌ Failed to connect to server');
    }
    setTestingGmail(false);
  };

  const handleConfigureGmail = async (e) => {
    e.preventDefault();
    setTestingGmail(true);
    setGmailError('');
    setGmailSuccess('');
    try {
      const res = await fetch(`${API}/api/gmail/configure`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(gmailForm),
      });
      const data = await res.json();
      if (res.ok) {
        setGmailSuccess('✅ Gmail account connected and configured!');
        fetchGmailStatus();
      } else {
        setGmailError(`❌ Configuration failed: ${data.detail || data.error}`);
      }
    } catch (err) {
      setGmailError('❌ Failed to connect to server');
    }
    setTestingGmail(false);
  };

  const fetchAccounts = async () => {
    try {
      const res = await fetch(`${API}/api/accounts`);
      setAccounts(await res.json());
    } catch (err) { console.error(err); }
  };

  const handleAdd = async (e) => {
    e.preventDefault();
    if (!form.email_address || !form.app_password) return;
    setAdding(true);
    try {
      await fetch(`${API}/api/accounts`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...form, provider }),
      });
      setForm({ email_address: '', display_name: '', app_password: '' });
      setShowForm(false);
      fetchAccounts();
    } catch (err) { console.error(err); }
    setAdding(false);
  };

  const handleDelete = async (id) => {
    if (!confirm('Remove this email account?')) return;
    await fetch(`${API}/api/accounts/${id}`, { method: 'DELETE' });
    fetchAccounts();
  };

  return (
    <div className="main-content animate-in">
      {/* V5.0 Active Gmail Card */}
      <div className="glass-card no-hover" style={{ marginBottom: 24, padding: 20 }}>
        <h3 style={{ marginBottom: 12, fontSize: '1.1rem', fontWeight: 700, display: 'flex', alignItems: 'center', gap: 8 }}>
          🔴 Active Real Gmail Connection
          <span className={`badge ${gmailStatus.status === 'connected' ? 'badge-success' : 'badge-danger'}`} style={{ fontSize: '0.7rem', padding: '2px 8px' }}>
            {gmailStatus.status?.toUpperCase()}
          </span>
        </h3>
        <p style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', marginBottom: 16 }}>
          Connect your Google Account using a 16-character Gmail App Password. This will replace the demo email sender with your active Gmail to send real campaign emails.
        </p>

        <form onSubmit={handleConfigureGmail} style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr auto', gap: 12, alignItems: 'end' }}>
          <div className="form-group" style={{ margin: 0 }}>
            <label className="form-label">Gmail Address</label>
            <input className="form-input" placeholder="you@gmail.com" value={gmailForm.email} onChange={e => setGmailForm({...gmailForm, email: e.target.value})} required />
          </div>
          <div className="form-group" style={{ margin: 0 }}>
            <label className="form-label">Display Name</label>
            <input className="form-input" placeholder="DMCAShield Team" value={gmailForm.display_name} onChange={e => setGmailForm({...gmailForm, display_name: e.target.value})} required />
          </div>
          <div className="form-group" style={{ margin: 0 }}>
            <label className="form-label">Gmail App Password</label>
            <input className="form-input" type="password" placeholder="xxxx xxxx xxxx xxxx" value={gmailForm.app_password} onChange={e => setGmailForm({...gmailForm, app_password: e.target.value})} required />
          </div>
          <div style={{ display: 'flex', gap: 8 }}>
            <button className="btn btn-secondary" type="button" onClick={handleTestGmail} disabled={testingGmail || !gmailForm.email || !gmailForm.app_password}>
              Test Connection
            </button>
            <button className="btn btn-primary" type="submit" disabled={testingGmail}>
              {gmailStatus.status === 'connected' ? 'Update Credentials' : 'Connect Account'}
            </button>
          </div>
        </form>

        {gmailError && (
          <div style={{ marginTop: 16, padding: 12, borderRadius: 'var(--radius-sm)', background: 'rgba(239, 68, 68, 0.1)', border: '1px solid rgba(239, 68, 68, 0.2)', fontSize: '0.8rem', color: '#ef4444' }}>
            {gmailError}
          </div>
        )}
        {gmailSuccess && (
          <div style={{ marginTop: 16, padding: 12, borderRadius: 'var(--radius-sm)', background: 'rgba(16, 185, 129, 0.1)', border: '1px solid rgba(16, 185, 129, 0.2)', fontSize: '0.8rem', color: '#10b981' }}>
            {gmailSuccess}
          </div>
        )}
      </div>

      <div className="page-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <div>
          <h1>📧 Email Accounts</h1>
          <p>Manage Gmail, Resend, and other sending accounts</p>
        </div>
        <button className="btn btn-primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? '✕ Cancel' : '➕ Add Account'}
        </button>
      </div>

      {showForm && (
        <div className="glass-card no-hover animate-in" style={{ marginBottom: 20 }}>
          <h3 style={{ marginBottom: 16, fontSize: '1rem', fontWeight: 700 }}>🔐 Add Email Provider</h3>
          
          <div style={{ display: 'flex', gap: 12, marginBottom: 16 }}>
            {[
              { id: 'gmail', icon: '📧', label: 'Gmail' },
              { id: 'resend', icon: '🔵', label: 'Resend (Free 10k/mo)' },
              { id: 'sendgrid', icon: '🟣', label: 'SendGrid' },
            ].map(p => (
              <button key={p.id} className={`btn ${provider === p.id ? 'btn-primary' : ''}`}
                style={{ background: provider === p.id ? 'var(--accent-primary)' : 'var(--bg-tertiary)', padding: '10px 16px' }}
                onClick={() => setProvider(p.id)}>
                {p.icon} {p.label}
              </button>
            ))}
          </div>

          {provider === 'resend' ? (
            <form onSubmit={handleAdd}>
              <div className="form-group">
                <label className="form-label">Resend API Key</label>
                <input className="form-input" placeholder="re_xxxx..." value={form.app_password} onChange={e => setForm({...form, app_password: e.target.value})} />
              </div>
              <div className="form-group">
                <label className="form-label">From Email</label>
                <input className="form-input" placeholder="your@domain.com" value={form.email_address} onChange={e => setForm({...form, email_address: e.target.value})} />
              </div>
              <div className="form-group">
                <label className="form-label">From Name</label>
                <input className="form-input" placeholder="Your Name" value={form.display_name} onChange={e => setForm({...form, display_name: e.target.value})} />
              </div>
              <button className="btn btn-success" type="submit" disabled={adding}>{adding ? '...' : '✅ Add Resend'}</button>
            </form>
          ) : (
            <form onSubmit={handleAdd} style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr auto', gap: 12, alignItems: 'end' }}>
              <div className="form-group" style={{ margin: 0 }}>
                <label className="form-label">{provider === 'sendgrid' ? 'API Key' : 'Email Address'}</label>
                <input className="form-input" placeholder={provider === 'sendgrid' ? 'SG.xxx' : 'you@gmail.com'} value={form.email_address} onChange={e => setForm({...form, email_address: e.target.value})} />
              </div>
              <div className="form-group" style={{ margin: 0 }}>
                <label className="form-label">Display Name</label>
                <input className="form-input" placeholder="John Smith" value={form.display_name} onChange={e => setForm({...form, display_name: e.target.value})} />
              </div>
              <div className="form-group" style={{ margin: 0 }}>
                <label className="form-label">{provider === 'sendgrid' ? 'API Key' : 'App Password'}</label>
                <input className="form-input" type="password" placeholder="xxxx xxxx xxxx xxxx" value={form.app_password} onChange={e => setForm({...form, app_password: e.target.value})} />
              </div>
              <button className="btn btn-success" type="submit" disabled={adding}>{adding ? '...' : '✅ Add'}</button>
            </form>
          )}
        </div>
      )}

      <div className="glass-card no-hover">
        {accounts.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon">📧</div>
            <h3>No email accounts connected</h3>
            <p style={{ color: 'var(--text-tertiary)' }}>Add Gmail, Resend, or SendGrid to send outreach emails</p>
          </div>
        ) : (
          <table className="data-table">
            <thead><tr><th>Provider</th><th>Email</th><th>Status</th><th>Sent Today</th><th>Health</th><th>Actions</th></tr></thead>
            <tbody>
              {accounts.map(acc => (
                <tr key={acc.id}>
                  <td><span className="badge" style={{ background: acc.provider === 'resend' ? '#3b82f6' : acc.provider === 'sendgrid' ? '#8b5cf6' : '#ef4444' }}>
                    {acc.provider?.toUpperCase() || 'GMAIL'}
                  </span></td>
                  <td><strong>{acc.email_address}</strong><br/><span style={{ fontSize: '0.7rem', color: 'var(--text-tertiary)' }}>{acc.display_name}</span></td>
                  <td><span className={`badge ${acc.status === 'active' ? 'badge-active' : acc.status === 'warming_up' ? 'badge-warm' : 'badge-error'}`}>{acc.status}</span></td>
                  <td>{acc.sent_today || 0}/{acc.daily_limit || 500}</td>
                  <td>
                    <div className="progress-bar" style={{ width: 60 }}>
                      <div className="progress-fill" style={{ width: `${acc.health_score || 100}%`, background: 'var(--accent-success)' }} />
                    </div>
                  </td>
                  <td><button className="btn btn-danger" style={{ padding: '4px 10px', fontSize: '0.72rem' }} onClick={() => handleDelete(acc.id)}>Remove</button></td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
