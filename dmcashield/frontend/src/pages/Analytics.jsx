import { useState, useEffect } from 'react';
const API = 'http://localhost:8000';

export default function Analytics() {
  const [data, setData] = useState(null);
  const [topSubjects, setTopSubjects] = useState([]);
  const [leadScores, setLeadScores] = useState([]);
  const [timeRange, setTimeRange] = useState('7d');

  useEffect(() => {
    fetch(`${API}/api/analytics`).then(r => r.json()).then(setData).catch(console.error);
    fetch(`${API}/api/analytics/top-subjects`).then(r => r.json()).then(setTopSubjects).catch(console.error);
    fetch(`${API}/api/leads/scored`).then(r => r.json()).then(setLeadScores).catch(() => setLeadScores([]));
  }, [timeRange]);

  if (!data) return <div className="main-content"><div className="empty-state"><div className="empty-icon">⏳</div><h3>Loading analytics...</h3></div></div>;

  // Calculate conversion rates
  const openRate = data.total_emails_sent ? (data.total_opened / data.total_emails_sent * 100).toFixed(1) : 0;
  const replyRate = data.total_emails_sent ? (data.total_replied / data.total_emails_sent * 100).toFixed(1) : 0;
  const convRate = data.total_opened ? (data.converted / data.total_opened * 100).toFixed(1) : 0;
  const hotRate = data.total_leads ? (data.hot_leads / data.total_leads * 100).toFixed(1) : 0;

  return (
    <div className="main-content animate-in">
      <div className="page-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <div>
          <h1>📈 Analytics</h1>
          <p>Campaign performance, engagement metrics, and funnel analysis</p>
        </div>
        <div style={{ display: 'flex', gap: 8 }}>
          {['7d', '30d', '90d', 'all'].map(t => (
            <button key={t} className={`btn ${timeRange === t ? 'btn-primary' : ''}`}
              style={{ padding: '8px 14px', background: timeRange === t ? 'var(--accent-primary)' : 'var(--bg-tertiary)', fontSize: '0.76rem' }}
              onClick={() => setTimeRange(t)}>
              {t === 'all' ? 'All Time' : t}
            </button>
          ))}
        </div>
      </div>

      {/* Key Metrics */}
      <div className="stats-grid">
        <div className="stat-card purple">
          <div className="stat-label">Total Leads</div>
          <div className="stat-value purple">{data.total_leads || 0}</div>
          <div style={{ fontSize: '0.68rem', color: 'var(--text-tertiary)', marginTop: 4 }}>+12% this week</div>
        </div>
        <div className="stat-card teal">
          <div className="stat-label">Emails Sent</div>
          <div className="stat-value teal">{data.total_emails_sent || 0}</div>
        </div>
        <div className="stat-card green">
          <div className="stat-label">Open Rate</div>
          <div className="stat-value green">{openRate}%</div>
          <div style={{ fontSize: '0.68rem', color: Number(openRate) > 30 ? 'var(--accent-success)' : 'var(--accent-warning)', marginTop: 4 }}>
            {Number(openRate) > 30 ? '✓ Good' : '⚠ Below avg'}
          </div>
        </div>
        <div className="stat-card orange">
          <div className="stat-label">Reply Rate</div>
          <div className="stat-value orange">{replyRate}%</div>
        </div>
        <div className="stat-card red">
          <div className="stat-label">Hot Leads</div>
          <div className="stat-value red">{data.hot_leads || 0}</div>
          <div style={{ fontSize: '0.68rem', color: 'var(--text-tertiary)', marginTop: 4 }}>{hotRate}% of total</div>
        </div>
        <div className="stat-card green">
          <div className="stat-label">Converted</div>
          <div className="stat-value green">{data.converted || 0}</div>
          <div style={{ fontSize: '0.68rem', color: 'var(--text-tertiary)', marginTop: 4 }}>{convRate}% open rate</div>
        </div>
      </div>

      <div className="grid-2">
        {/* Funnel */}
        <div className="glass-card no-hover">
          <h3 style={{ marginBottom: 16, fontSize: '1rem', fontWeight: 700 }}>📊 Conversion Funnel</h3>
          {[
            { label: 'Leads Generated', value: data.total_leads || 0, color: 'var(--accent-info)', pct: 100 },
            { label: 'Emails Delivered', value: data.total_emails_sent || 0, color: 'var(--accent-primary)', pct: data.total_leads ? Math.round((data.total_emails_sent / data.total_leads) * 100) : 0 },
            { label: 'Emails Opened', value: data.total_opened || 0, color: 'var(--accent-secondary)', pct: data.total_emails_sent ? Math.round((data.total_opened / data.total_emails_sent) * 100) : 0 },
            { label: 'Replied', value: data.total_replied || 0, color: 'var(--accent-warning)', pct: data.total_opened ? Math.round((data.total_replied / data.total_opened) * 100) : 0 },
            { label: 'Hot Leads', value: data.hot_leads || 0, color: 'var(--accent-hot)', pct: data.total_replied ? Math.round((data.hot_leads / data.total_replied) * 100) : 0 },
            { label: 'Converted', value: data.converted || 0, color: 'var(--accent-success)', pct: data.hot_leads ? Math.round((data.converted / data.hot_leads) * 100) : 0 },
          ].map((s, i) => (
            <div key={i} style={{ marginBottom: 10 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.78rem', marginBottom: 4 }}>
                <span style={{ color: 'var(--text-secondary)' }}>{s.label}</span>
                <span style={{ fontWeight: 700, color: s.color }}>{s.value?.toLocaleString() || 0} <span style={{ color: 'var(--text-tertiary)', fontWeight: 400 }}>({s.pct}%)</span></span>
              </div>
              <div className="progress-bar" style={{ height: 8 }}>
                <div className="progress-fill" style={{ width: `${s.pct}%`, background: s.color, borderRadius: 4 }} />
              </div>
            </div>
          ))}
        </div>

        {/* Top Subjects */}
        <div className="glass-card no-hover">
          <h3 style={{ marginBottom: 16, fontSize: '1rem', fontWeight: 700 }}>🏆 Top Subject Lines</h3>
          {topSubjects.length === 0 ? (
            <div style={{ color: 'var(--text-tertiary)', fontSize: '0.82rem', textAlign: 'center', padding: 20 }}>No email data yet</div>
          ) : (
            topSubjects.slice(0, 5).map((s, i) => (
              <div key={i} style={{ padding: '10px 0', borderBottom: '1px solid var(--border-subtle)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div style={{ fontSize: '0.82rem', maxWidth: '70%', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                  <span style={{ color: 'var(--text-tertiary)', marginRight: 8 }}>#{i + 1}</span>
                  {s.subject}
                </div>
                <div style={{ fontSize: '0.72rem', color: 'var(--accent-success)', fontFamily: 'var(--font-mono)' }}>
                  {s.opens || 0} / {s.sends || 0}
                </div>
              </div>
            ))
          )}
        </div>
      </div>

      {/* Lead Scoring */}
      {leadScores.length > 0 && (
        <div className="glass-card no-hover" style={{ marginTop: 20 }}>
          <h3 style={{ marginBottom: 16, fontSize: '1rem', fontWeight: 700 }}>🎯 High Score Leads</h3>
          <table className="data-table">
            <thead><tr><th>Business</th><th>Score</th><th>City</th><th>Email</th><th>Action</th></tr></thead>
            <tbody>
              {leadScores.slice(0, 10).map((lead, i) => (
                <tr key={i}>
                  <td><strong>{lead.business_name}</strong></td>
                  <td><span className="badge badge-active">{lead.lead_score}</span></td>
                  <td>{lead.city}</td>
                  <td style={{ color: 'var(--text-secondary)' }}>{lead.email_primary}</td>
                  <td><button className="btn btn-primary" style={{ padding: '4px 10px', fontSize: '0.72rem' }}>Email</button></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
