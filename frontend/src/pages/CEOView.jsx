import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

import API from '../config/api.js';

export default function CEOView() {
  const [overview, setOverview] = useState(null);
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [commandInput, setCommandInput] = useState('');
  const [commandDept, setCommandDept] = useState('marketing');
  const [commandResult, setCommandResult] = useState('');
  const [costOpt, setCostOpt] = useState(null);

  useEffect(() => {
    loadAll();
    const interval = setInterval(loadAll, 15000);
    return () => clearInterval(interval);
  }, []);

  const loadAll = async () => {
    try {
      const [ov, msgs, cost] = await Promise.all([
        fetch(`${API}/api/ceo/overview`).then(r => r.json()).catch(() => null),
        fetch(`${API}/api/messages/feed?limit=30`).then(r => r.json()).catch(() => ({ messages: [] })),
        fetch(`${API}/api/knowledge/cost-optimization`).then(r => r.json()).catch(() => null)
      ]);
      if (ov) setOverview(ov);
      setMessages(msgs.messages || []);
      if (cost) setCostOpt(cost);
    } catch (e) { console.error(e); }
    setLoading(false);
  };

  const sendCommand = async (e) => {
    e.preventDefault();
    if (!commandInput.trim()) return;
    try {
      const r = await fetch(`${API}/api/departments/${commandDept}/command`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ command: commandInput })
      });
      const data = await r.json();
      setCommandResult(`✅ Command sent to ${commandDept}: "${commandInput}"`);
      setCommandInput('');
      setTimeout(() => setCommandResult(''), 5000);
    } catch {
      setCommandResult('❌ Failed to send command');
    }
  };

  if (loading) {
    return (
      <main className="main-content" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
        <div style={{ textAlign: 'center' }}>
          <div style={{ fontSize: '3rem' }}>🏢</div>
          <p className="text-secondary">Loading CEO Overview...</p>
        </div>
      </main>
    );
  }

  const soul = overview?.soul || {};
  const dbStats = overview?.db_stats || {};
  const learning = overview?.learning || {};
  const deptStatuses = overview?.department_statuses || {};
  const deptIcons = {
    scraping: '🕵️', validation: '✅', marketing: '📣', sending: '📧',
    analytics: '📊', sales: '💰', sheets: '📋', accounts: '👤',
    tasks: '📌', ml: '🤖', jarvis: '🧠', memory: '💾'
  };

  return (
    <main className="main-content">
      <div className="page-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h1>👔 CEO Command Center</h1>
          <p className="text-secondary">Full company overview — see everything, control everything</p>
        </div>
        <button onClick={loadAll} className="btn btn-primary">🔄 Refresh</button>
      </div>

      {/* Top Stats */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-number" style={{ color: 'var(--success)' }}>{overview?.status || 'operational'}</div>
          <div className="stat-label">Company Status</div>
        </div>
        <div className="stat-card">
          <div className="stat-number">{overview?.departments_active || 0}</div>
          <div className="stat-label">Departments</div>
        </div>
        <div className="stat-card">
          <div className="stat-number">{overview?.agents_active || 0}</div>
          <div className="stat-label">Active Agents</div>
        </div>
        <div className="stat-card">
          <div className="stat-number" style={{ color: 'var(--danger)' }}>{dbStats.hot_leads || 0}</div>
          <div className="stat-label">Hot Leads</div>
        </div>
      </div>

      <div className="stats-grid" style={{ gridTemplateColumns: 'repeat(4, 1fr)', marginTop: '0.5rem' }}>
        <div className="stat-card">
          <div className="stat-number">{dbStats.total_leads || 0}</div>
          <div className="stat-label">Total Leads</div>
        </div>
        <div className="stat-card">
          <div className="stat-number">{dbStats.total_emails || 0}</div>
          <div className="stat-label">Emails Sent</div>
        </div>
        <div className="stat-card">
          <div className="stat-number">{dbStats.active_tasks || 0}</div>
          <div className="stat-label">Active Tasks</div>
        </div>
        <div className="stat-card">
          <div className="stat-number" style={{ color: 'var(--primary)' }}>{learning.cycle || 0}</div>
          <div className="stat-label">Learning Cycles</div>
        </div>
      </div>

      {/* Departments Grid */}
      <div className="card" style={{ margin: '1.5rem 0' }}>
        <h2 style={{ marginBottom: '1rem' }}>🏢 All Departments</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(180px, 1fr))', gap: '0.75rem' }}>
          {Object.entries(deptStatuses).map(([name, info]) => (
            <Link key={name} to={`/department/${name}`} style={{ textDecoration: 'none' }}>
              <div className="card" style={{
                textAlign: 'center', padding: '1rem', cursor: 'pointer',
                borderLeft: `3px solid ${info?.head?.status === 'active' || info?.head?.status === 'online' ? 'var(--success)' : 'var(--warning)'}`,
                transition: 'transform 0.2s'
              }}
                onMouseEnter={e => e.currentTarget.style.transform = 'scale(1.02)'}
                onMouseLeave={e => e.currentTarget.style.transform = 'scale(1)'}>
                <div style={{ fontSize: '2rem' }}>{deptIcons[name] || '📦'}</div>
                <div style={{ fontWeight: 700, textTransform: 'capitalize', marginTop: '0.3rem' }}>{name}</div>
                <div style={{ fontSize: '0.75rem', color: 'var(--success)', marginTop: '0.15rem' }}>
                  ● {info?.head?.status || 'online'} • {(info?.team?.length || 0) + 1} agents
                </div>
                <div className="text-secondary" style={{ fontSize: '0.7rem', marginTop: '0.2rem' }}>
                  Tasks: {info?.head?.tasks_completed || 0}
                </div>
              </div>
            </Link>
          ))}
        </div>
      </div>

      {/* Command Center + Message Feed side by side */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
        {/* CEO Command Panel */}
        <div className="card">
          <h2 style={{ marginBottom: '1rem' }}>⚡ Quick Commands</h2>
          <form onSubmit={sendCommand} style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            <select value={commandDept} onChange={e => setCommandDept(e.target.value)}
              style={{
                padding: '0.75rem', borderRadius: '10px', background: 'rgba(255,255,255,0.06)',
                border: '1px solid rgba(255,255,255,0.1)', color: 'var(--text-primary)', fontSize: '0.9rem'
              }}>
              {Object.keys(deptStatuses).map(d => (
                <option key={d} value={d}>{deptIcons[d] || '📦'} {d}</option>
              ))}
            </select>
            <input value={commandInput} onChange={e => setCommandInput(e.target.value)}
              placeholder='Command (e.g., "pause sending", "focus on dentists")'
              style={{
                padding: '0.75rem', borderRadius: '10px', background: 'rgba(255,255,255,0.06)',
                border: '1px solid rgba(255,255,255,0.1)', color: 'var(--text-primary)', fontSize: '0.9rem', outline: 'none'
              }} />
            <button className="btn btn-primary" type="submit">📡 Send Command</button>
            {commandResult && (
              <div style={{ padding: '0.5rem', borderRadius: '8px', background: 'rgba(16,185,129,0.1)', fontSize: '0.85rem', color: 'var(--success)' }}>
                {commandResult}
              </div>
            )}
          </form>

          <div style={{ marginTop: '1rem' }}>
            <div className="text-secondary" style={{ fontSize: '0.8rem', marginBottom: '0.5rem' }}>Quick Actions:</div>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.4rem' }}>
              {['pause sending', 'resume sending', 'run learning cycle', 'export leads', 'focus on Houston'].map(cmd => (
                <button key={cmd} className="btn" onClick={() => { setCommandInput(cmd); }}
                  style={{ fontSize: '0.75rem', padding: '0.3rem 0.6rem' }}>
                  {cmd}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Inter-Department Message Feed */}
        <div className="card">
          <h2 style={{ marginBottom: '1rem' }}>📨 Agent Communications ({messages.length})</h2>
          <div style={{ maxHeight: '350px', overflowY: 'auto' }}>
            {messages.length === 0 ? (
              <p className="text-secondary" style={{ textAlign: 'center', padding: '2rem' }}>
                No inter-department messages yet — launch a task to see agents communicate
              </p>
            ) : (
              messages.slice().reverse().map((m, i) => (
                <div key={i} style={{
                  padding: '0.6rem', borderRadius: '8px', marginBottom: '0.4rem',
                  background: m.priority === 'high' ? 'rgba(239,68,68,0.1)' : 'rgba(255,255,255,0.03)',
                  borderLeft: `3px solid ${m.priority === 'high' ? 'var(--danger)' : m.message_type === 'handoff' ? 'var(--warning)' : 'var(--primary)'}`
                }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem' }}>
                    <span><strong>{m.from}</strong> → <strong>{m.to}</strong></span>
                    <span className="text-secondary">{m.message_type}</span>
                  </div>
                  {m.notes && <div style={{ fontSize: '0.8rem', marginTop: '0.2rem', color: 'var(--text-secondary)' }}>{m.notes}</div>}
                </div>
              ))
            )}
          </div>
        </div>
      </div>

      {/* Soul / Learning Stats & Cost Widget */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem', marginTop: '1.5rem' }}>
        {/* Soul / Learning Stats */}
        <div className="card" style={{ margin: 0 }}>
          <h2 style={{ marginBottom: '1rem' }}>🧠 Company Intelligence</h2>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '1.5rem', alignItems: 'center' }}>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '2rem', fontWeight: 700, color: 'var(--primary)' }}>{soul.learning_cycle || learning.cycle || 0}</div>
              <div className="text-secondary" style={{ fontSize: '0.8rem' }}>Learning Cycles</div>
            </div>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '2rem', fontWeight: 700, color: 'var(--success)' }}>{soul.total_emails_sent || 0}</div>
              <div className="text-secondary" style={{ fontSize: '0.8rem' }}>Total Emails</div>
            </div>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '2rem', fontWeight: 700, color: 'var(--warning)' }}>{soul.total_leads_processed || 0}</div>
              <div className="text-secondary" style={{ fontSize: '0.8rem' }}>Leads Processed</div>
            </div>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '2rem', fontWeight: 700, color: 'var(--danger)' }}>{soul.total_clients_acquired || 0}</div>
              <div className="text-secondary" style={{ fontSize: '0.8rem' }}>Clients Acquired</div>
            </div>
          </div>
          {learning.rules > 0 && (
            <div style={{ marginTop: '1rem', padding: '0.75rem', background: 'rgba(139,92,246,0.1)', borderRadius: '8px' }}>
              <span style={{ fontSize: '0.85rem' }}>🤖 ML Engine has discovered <strong>{learning.rules}</strong> optimization rules with avg open rate of <strong>{learning.avg_open_rate}%</strong></span>
            </div>
          )}
        </div>

        {/* Cost Optimization Card */}
        <div className="card" style={{ margin: 0 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
            <h2>💵 Cost & Budget</h2>
            {costOpt && (
              <span className="badge badge-active" style={{ background: 'var(--accent-success)' }}>
                Saving {costOpt.total_monthly_savings}
              </span>
            )}
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            {costOpt?.strategies.slice(0, 3).map((s, i) => (
              <div key={i} style={{ padding: '0.6rem', borderRadius: '8px', background: 'rgba(255,255,255,0.02)', borderLeft: '3px solid var(--accent-primary)' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.82rem', fontWeight: 700 }}>
                  <span>{s.area}</span>
                  <span style={{ color: 'var(--success)' }}>{s.savings}</span>
                </div>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', marginTop: '0.2rem' }}>
                  {s.method} ({s.source.split(':')[0]})
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </main>
  );
}
