import { useState, useEffect } from 'react';
import API from '../config/api.js';

export default function SystemDashboard() {
  const [status, setStatus] = useState(null);
  const [leads, setLeads] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [campaigns, setCampaigns] = useState([]);
  const [loading, setLoading] = useState(true);
  const [lastUpdate, setLastUpdate] = useState(null);

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 30000);
    return () => clearInterval(interval);
  }, []);

  const loadData = async () => {
    setLoading(true);
    setLastUpdate(new Date().toLocaleTimeString());
    try {
      const [s, l, t, c] = await Promise.all([
        fetch(`${API}/api/status`).then(r => r.json()).catch(() => null),
        fetch(`${API}/api/leads`).then(r => r.json()).catch(() => []),
        fetch(`${API}/api/tasks`).then(r => r.json()).catch(() => []),
        fetch(`${API}/api/campaigns`).then(r => r.json()).catch(() => [])
      ]);
      setStatus(s);
      setLeads(Array.isArray(l) ? l : []);
      setTasks(Array.isArray(t) ? t : []);
      setCampaigns(Array.isArray(c) ? c : []);
    } catch (e) {
      console.error(e);
    }
    setLoading(false);
  };

  if (loading && !status) {
    return (
      <main className="main-content" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <div style={{ textAlign: 'center' }}>
          <div style={{ fontSize: '3rem', marginBottom: '1rem', animation: 'spin 2s linear infinite' }}>⏳</div>
          <div style={{ fontSize: '1.2rem', color: 'var(--text-secondary)' }}>Loading Control Tower...</div>
        </div>
      </main>
    );
  }

  const isConnected = status && (status.system_status || status.departments);
  const depts = status?.departments || {};
  const deptEntries = Object.entries(depts);
  const stats = status?.soul || {};
  const hotCount = leads.filter(l => l.lead_temperature === 'hot').length;
  const deptIcons = {
    scraping: '🕵️', validation: '✅', marketing: '📣', sending: '📧',
    analytics: '📊', sales: '💰', sheets: '📋', accounts: '👤',
    tasks: '📌', ml: '🤖', jarvis: '🧠', memory: '💾'
  };

  return (
    <main className="main-content">
      <div className="page-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap' }}>
        <div>
          <h1>🏢 DMCAShield Control Tower</h1>
          <p className="text-secondary">Autonomous Agency • Real-Time System View</p>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <span className="text-secondary" style={{ fontSize: '0.85rem' }}>
            {lastUpdate ? `Updated: ${lastUpdate}` : ''}
          </span>
          <button onClick={loadData} className="btn btn-primary">🔄 Refresh</button>
        </div>
      </div>

      {/* Connection Status Banner */}
      <div className="card" style={{
        borderLeft: `4px solid ${isConnected ? 'var(--success)' : 'var(--warning)'}`,
        marginBottom: '1.5rem', padding: '1rem 1.5rem'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          <span style={{
            width: 10, height: 10, borderRadius: '50%',
            background: isConnected ? 'var(--success)' : 'var(--warning)',
            boxShadow: isConnected ? '0 0 8px var(--success)' : 'none'
          }}></span>
          <strong style={{ color: isConnected ? 'var(--success)' : 'var(--warning)' }}>
            {isConnected ? '✅ CONNECTED — Live Data' : '⚠️ DEMO MODE — Start backend for live data'}
          </strong>
        </div>
        <p className="text-secondary" style={{ margin: '0.25rem 0 0 1.5rem', fontSize: '0.85rem' }}>
          Backend: {API} • {deptEntries.length} departments online
        </p>
      </div>

      {/* Stats Grid */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-number" style={{ color: 'var(--success)' }}>
            {status?.system_status || 'operational'}
          </div>
          <div className="stat-label">System Status</div>
        </div>
        <div className="stat-card">
          <div className="stat-number">{deptEntries.length || 12}</div>
          <div className="stat-label">Departments</div>
        </div>
        <div className="stat-card">
          <div className="stat-number">{leads.length || stats.total_leads_processed || 0}</div>
          <div className="stat-label">Total Leads</div>
        </div>
        <div className="stat-card">
          <div className="stat-number" style={{ color: 'var(--danger)' }}>{hotCount}</div>
          <div className="stat-label">Hot Leads</div>
        </div>
      </div>

      {/* Departments Grid */}
      <div className="card" style={{ marginBottom: '1.5rem' }}>
        <h2 style={{ marginBottom: '1rem' }}>🏢 Departments ({deptEntries.length})</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(150px, 1fr))', gap: '0.75rem' }}>
          {deptEntries.length > 0 ? deptEntries.map(([name, info]) => {
            const headStatus = info?.head?.status || 'online';
            const teamSize = info?.team_size || (info?.head ? 3 : 0);
            return (
              <div key={name} className="card" style={{
                textAlign: 'center', padding: '1rem',
                borderLeft: `3px solid ${headStatus === 'online' ? 'var(--success)' : 'var(--danger)'}`
              }}>
                <div style={{ fontSize: '1.8rem', marginBottom: '0.3rem' }}>{deptIcons[name] || '📦'}</div>
                <div style={{ fontWeight: 600, textTransform: 'capitalize', fontSize: '0.85rem' }}>
                  {name.replace(/_/g, ' ')}
                </div>
                <div style={{ fontSize: '0.75rem', color: headStatus === 'online' ? 'var(--success)' : 'var(--danger)', marginTop: '0.25rem' }}>
                  ● {headStatus} • {teamSize}
                </div>
              </div>
            );
          }) : (
            <p className="text-secondary">No departments loaded</p>
          )}
        </div>
      </div>

      {/* Active Tasks & Campaigns Side-by-Side */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
        <div className="card">
          <h2 style={{ marginBottom: '1rem' }}>📋 Active Tasks ({tasks.length})</h2>
          {tasks.length > 0 ? (
            <table className="data-table">
              <thead><tr><th>Task</th><th>Status</th><th>Leads</th></tr></thead>
              <tbody>
                {tasks.map(t => (
                  <tr key={t.id}>
                    <td><strong>{t.business_type || t.title}</strong> — {t.city}</td>
                    <td><span className="badge" style={{
                      background: t.status === 'active' ? 'rgba(16,185,129,0.2)' : 'rgba(100,100,100,0.2)',
                      color: t.status === 'active' ? 'var(--success)' : 'var(--text-secondary)'
                    }}>{t.status}</span></td>
                    <td>{t.leads_total || 0}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p className="text-secondary" style={{ textAlign: 'center', padding: '2rem' }}>No active tasks — launch one from the sidebar</p>
          )}
        </div>

        <div className="card">
          <h2 style={{ marginBottom: '1rem' }}>📣 Campaigns ({campaigns.length})</h2>
          {campaigns.length > 0 ? (
            <table className="data-table">
              <thead><tr><th>Campaign</th><th>Status</th><th>Leads</th></tr></thead>
              <tbody>
                {campaigns.map(c => (
                  <tr key={c.id}>
                    <td><strong>{c.name}</strong></td>
                    <td><span className="badge" style={{
                      background: 'rgba(16,185,129,0.2)', color: 'var(--success)'
                    }}>{c.status}</span></td>
                    <td>{c.leads_total || c.sent || 0}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p className="text-secondary" style={{ textAlign: 'center', padding: '2rem' }}>No campaigns yet</p>
          )}
        </div>
      </div>

      {/* Learning Engine Stats */}
      {stats.learning_cycle && (
        <div className="card" style={{ marginTop: '1.5rem' }}>
          <h2 style={{ marginBottom: '1rem' }}>🧠 Self-Learning Engine</h2>
          <div className="stats-grid" style={{ gridTemplateColumns: 'repeat(4, 1fr)' }}>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '1.8rem', fontWeight: 700, color: 'var(--primary)' }}>{stats.learning_cycle}</div>
              <div className="text-secondary" style={{ fontSize: '0.8rem' }}>Learning Cycles</div>
            </div>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '1.8rem', fontWeight: 700, color: 'var(--success)' }}>{stats.total_emails_sent || 0}</div>
              <div className="text-secondary" style={{ fontSize: '0.8rem' }}>Emails Sent</div>
            </div>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '1.8rem', fontWeight: 700, color: 'var(--warning)' }}>{stats.total_leads_processed || 0}</div>
              <div className="text-secondary" style={{ fontSize: '0.8rem' }}>Leads Processed</div>
            </div>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '1.8rem', fontWeight: 700, color: 'var(--danger)' }}>{stats.total_clients_acquired || 0}</div>
              <div className="text-secondary" style={{ fontSize: '0.8rem' }}>Clients Acquired</div>
            </div>
          </div>
        </div>
      )}
    </main>
  );
}