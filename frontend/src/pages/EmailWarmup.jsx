import { useState, useEffect } from 'react';
import API from '../config/api.js';

export default function EmailWarmup() {
  const [accounts, setAccounts] = useState([]);
  const [selected, setSelected] = useState(null);
  const [warmupLogs, setWarmupLogs] = useState([]);
  const [autoWarmup, setAutoWarmup] = useState(true);

  useEffect(() => {
    fetchAccounts();
  }, []);

  const fetchAccounts = async () => {
    try {
      const res = await fetch(`${API}/api/accounts`);
      const data = await res.json();
      setAccounts(data);
      if (data.length > 0 && !selected) setSelected(data[0]);
    } catch {}
  };

  const startWarmup = async (accountId) => {
    await fetch(`${API}/api/accounts/${accountId}/warmup`, { method: 'POST' });
    fetchAccounts();
  };

  const stopWarmup = async (accountId) => {
    await fetch(`${API}/api/accounts/${accountId}/warmup`, { method: 'DELETE' });
    fetchAccounts();
  };

  // Simulate warmup logs (replace with real API in production)
  const logs = [
    { day: 1, sent: 5, opens: 3, replies: 0 },
    { day: 2, sent: 8, opens: 5, replies: 1 },
    { day: 3, sent: 12, opens: 8, replies: 2 },
    { day: 4, sent: 15, opens: 10, replies: 3 },
    { day: 5, sent: 18, opens: 14, replies: 4 },
  ];

  return (
    <div className="main-content animate-in">
      <div className="page-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <div>
          <h1>🔥 Email Warmup</h1>
          <p>Auto-warmup Gmail accounts for better deliverability</p>
        </div>
        <label style={{ display: 'flex', alignItems: 'center', gap: 10, cursor: 'pointer', background: 'var(--bg-tertiary)', padding: '10px 16px', borderRadius: 10 }}>
          <input type="checkbox" checked={autoWarmup} onChange={e => setAutoWarmup(e.target.checked)} />
          <span style={{ fontWeight: 600 }}>Auto Warmup</span>
        </label>
      </div>

      {/* Auto Warmup Settings */}
      <div className="glass-card no-hover" style={{ marginBottom: 20 }}>
        <h3 style={{ marginBottom: 16 }}>⚙️ Warmup Settings</h3>
        <div className="grid-2">
          <div className="form-group">
            <label className="form-label">Daily Send Limit</label>
            <input className="form-input" type="number" defaultValue={50} />
          </div>
          <div className="form-group">
            <label className="form-label">Randomize Timing</label>
            <select className="form-input">
              <option>Yes - Spread throughout day</option>
              <option>No - Fixed intervals</option>
            </select>
          </div>
        </div>
        <div className="grid-2">
          <div className="form-group">
            <label className="form-label">Reply Probability</label>
            <input className="form-input" type="number" defaultValue={30} />
          </div>
          <div className="form-group">
            <label className="form-label">Open Tracking</label>
            <select className="form-input">
              <option>Yes - Track opens</option>
              <option>No - blind send</option>
            </select>
          </div>
        </div>
        <button className="btn btn-primary">Save Settings</button>
      </div>

      {/* Accounts */}
      <div className="glass-card no-hover">
        <h3 style={{ marginBottom: 16 }}>📧 Account Status</h3>
        {accounts.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon">📧</div>
            <h3>No accounts to warmup</h3>
            <p style={{ color: 'var(--text-tertiary)' }}>Add email accounts first</p>
          </div>
        ) : (
          <div style={{ display: 'grid', gap: 12 }}>
            {accounts.map((acc, i) => (
              <div key={i} style={{ padding: 16, background: 'var(--bg-tertiary)', borderRadius: 12 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <div>
                    <div style={{ fontWeight: 600 }}>{acc.email_address}</div>
                    <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                      {acc.warmup_day ? `Day ${acc.warmup_day}/28` : 'Not started'} • {acc.sent_today || 0} sent today
                    </div>
                  </div>
                  <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
                    {/* Progress ring */}
                    <div style={{ position: 'relative', width: 50, height: 50 }}>
                      <svg viewBox="0 0 50 50" style={{ transform: 'rotate(-90deg)' }}>
                        <circle cx="25" cy="25" r="20" fill="none" stroke="var(--bg-secondary)" strokeWidth="4" />
                        <circle cx="25" cy="25" r="20" fill="none" stroke="var(--accent-success)" strokeWidth="4"
                          strokeDasharray={`${(acc.warmup_day || 0) / 28 * 125.6} 125.6`} />
                      </svg>
                      <span style={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', fontSize: '0.7rem', fontWeight: 700 }}>
                        {acc.warmup_day || 0}d
                      </span>
                    </div>
                    {acc.status === 'warming_up' ? (
                      <button className="btn btn-danger" onClick={() => stopWarmup(acc.id)}>Stop</button>
                    ) : (
                      <button className="btn btn-success" onClick={() => startWarmup(acc.id)}>Start</button>
                    )}
                  </div>
                </div>

                {/* Stats when active */}
                {acc.status === 'warming_up' && (
                  <div style={{ marginTop: 12, paddingTop: 12, borderTop: '1px solid var(--border-subtle)', display: 'flex', gap: 20 }}>
                    <div><span style={{ color: 'var(--text-tertiary)', fontSize: '0.76rem' }}>Sent</span><div style={{ fontWeight: 600 }}>{acc.sent_today || 0}</div></div>
                    <div><span style={{ color: 'var(--text-tertiary)', fontSize: '0.76rem' }}>Opens</span><div style={{ fontWeight: 600 }}>{Math.floor((acc.sent_today || 0) * 0.4)}</div></div>
                    <div><span style={{ color: 'var(--text-tertiary)', fontSize: '0.76rem' }}>Replies</span><div style={{ fontWeight: 6 }}>{(acc.sent_today || 0) * 0.05}</div></div>
                    <div><span style={{ color: 'var(--text-tertiary)', fontSize: '0.76rem' }}>Health</span><div style={{ fontWeight: 600, color: 'var(--accent-success)' }}>{acc.health_score || 100}%</div></div>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Warmup Guide */}
      <div className="glass-card no-hover" style={{ marginTop: 20 }}>
        <h3 style={{ marginBottom: 16 }}>📚 28-Day Warmup Guide</h3>
        {logs.map((log, i) => (
          <div key={i} style={{ padding: '8px 0', borderBottom: '1px solid var(--border-subtle)', display: 'flex', justifyContent: 'space-between' }}>
            <span style={{ color: 'var(--text-secondary)' }}>Day {log.day}</span>
            <span style={{ fontSize: '0.86rem' }}>{log.sent} emails • {log.opens} opens • {log.replies} replies</span>
          </div>
        ))}
      </div>
    </div>
  );
}