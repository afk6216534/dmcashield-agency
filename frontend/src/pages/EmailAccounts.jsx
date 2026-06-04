import { useState, useEffect } from 'react';
import API from '../config/api.js';

export default function EmailAccounts() {
  const [accounts, setAccounts] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [provider, setProvider] = useState('gmail');
  const [form, setForm] = useState({ email_address: '', display_name: '', app_password: '' });
  const [adding, setAdding] = useState(false);

  useEffect(() => { fetchAccounts(); }, []);

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
