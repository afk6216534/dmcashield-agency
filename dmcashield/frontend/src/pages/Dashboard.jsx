import { useState, useEffect } from 'react';

const API = 'http://localhost:8000';

const DEPT_ICONS = {
  scraping: '🔍', validation: '✅', marketing: '📢',
  sending: '📤', analytics: '📊', sales: '💼',
  sheets: '📋', accounts: '📧', tasks: '📝',
  ml: '🧠', jarvis: '🤖', memory: '💾',
};

export default function Dashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboard();
    const interval = setInterval(fetchDashboard, 15000);
    return () => clearInterval(interval);
  }, []);

  const fetchDashboard = async () => {
    try {
      const res = await fetch(`${API}/api/dashboard`);
      const json = await res.json();
      setData(json);
    } catch (err) {
      console.error('Dashboard fetch error:', err);
    }
    setLoading(false);
  };

  if (loading) return <div className="main-content"><div className="empty-state"><div className="empty-icon">⏳</div><h3>Loading Control Tower...</h3></div></div>;

  const stats = data?.stats || {};
  const soul = data?.soul || {};
  const departments = data?.departments || {};

  return (
    <div className="main-content animate-in">
      <div className="page-header">
        <h1>🛡️ DMCAShield Control Tower</h1>
        <p>Autonomous Agency Dashboard — {Object.keys(departments).length} departments, {data?.system_status || 'initializing'}</p>
      </div>

      {/* Stats Grid */}
      <div className="stats-grid">
        <div className="stat-card purple">
          <div className="stat-label">Emails Sent Today</div>
          <div className="stat-value purple">{stats.emails_sent_today || 0}</div>
          <div className="stat-change">📤 Outbound active</div>
        </div>
        <div className="stat-card teal">
          <div className="stat-label">Opens Today</div>
          <div className="stat-value teal">{stats.emails_opened_today || 0}</div>
          <div className="stat-change">👀 Engagement tracking</div>
        </div>
        <div className="stat-card green">
          <div className="stat-label">Replies Today</div>
          <div className="stat-value green">{stats.replies_today || 0}</div>
          <div className="stat-change">💬 Conversations active</div>
        </div>
        <div className="stat-card red">
          <div className="stat-label">Hot Leads</div>
          <div className="stat-value red">{stats.hot_leads || 0}</div>
          <div className="stat-change">🔥 Ready to convert</div>
        </div>
      </div>

      {/* Active Tasks - full width */}
      <div className="glass-card no-hover" style={{ marginBottom: 24 }}>
        <h3 style={{ marginBottom: 16, fontSize: '1rem', fontWeight: 700 }}>🎯 Active Tasks</h3>
        {(data?.active_tasks || []).length === 0 ? (
          <div className="empty-state" style={{ padding: 30 }}>
            <div className="empty-icon">🚀</div>
            <h3>No active tasks</h3>
            <p style={{ color: 'var(--text-tertiary)', fontSize: '0.82rem' }}>Go to Launch Task to start your first campaign</p>
          </div>
        ) : (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: 16 }}>
            {data.active_tasks.map((task) => (
              <div key={task.id} style={{ padding: 16, background: 'var(--bg-tertiary)', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-subtle)' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
                  <div>
                    <strong style={{ fontSize: '0.88rem' }}>{task.business_type}</strong>
                    <span style={{ color: 'var(--text-tertiary)', marginLeft: 8, fontSize: '0.78rem' }}>{task.city}, {task.state}</span>
                  </div>
                  <span className={`badge badge-${task.status}`}>{task.status}</span>
                </div>
                <div className="progress-bar" style={{ marginTop: 8 }}>
                  <div className="progress-fill" style={{ width: `${task.leads_total > 0 ? (task.leads_emailed / task.leads_total) * 100 : 0}%` }} />
                </div>
                <div style={{ fontSize: '0.7rem', color: 'var(--text-tertiary)', marginTop: 4 }}>
                  {task.leads_emailed || 0}/{task.leads_total || 0} leads emailed • {task.leads_hot || 0} hot
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Department Status - full width with all 12 departments */}
      <div className="glass-card no-hover" style={{ marginBottom: 24 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
          <h3 style={{ fontSize: '1rem', fontWeight: 700 }}>🏢 Department Status</h3>
          <span style={{ fontSize: '0.72rem', color: 'var(--accent-secondary)', fontFamily: 'var(--font-mono)' }}>
            {Object.keys(departments).length} departments • {Object.values(departments).reduce((a, d) => a + (d?.team_size || 0) + 1, 0)} agents
          </span>
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(140px, 1fr))', gap: 10 }}>
          {Object.entries(departments).map(([name, dept]) => {
            const deptStatus = dept?.head?.status || 'idle';
            const agentCount = (dept?.team_size || 0) + 1;
            const isOnline = deptStatus === 'idle' || deptStatus === 'working';
            const tasksCompleted = dept?.head?.tasks_completed || 0;
            return (
              <div className="dept-card" key={name} style={{ position: 'relative' }}>
                <div style={{ fontSize: '1.4rem' }}>{DEPT_ICONS[name] || '🔧'}</div>
                <div className="dept-name" style={{ textTransform: 'capitalize' }}>{name}</div>
                <div className="dept-status-label">
                  <span className={`status-dot ${isOnline ? 'green' : 'red'}`}></span>
                  {deptStatus === 'working' ? 'busy' : 'online'} • {agentCount}
                </div>
                {tasksCompleted > 0 && (
                  <div style={{ fontSize: '0.6rem', color: 'var(--accent-success)', marginTop: 2 }}>
                    {tasksCompleted} tasks done
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* Recent Activity & Soul - side by side */}
      <div className="grid-2">
        <div className="glass-card no-hover">
          <h3 style={{ marginBottom: 16, fontSize: '1rem', fontWeight: 700 }}>📡 Recent Activity</h3>
          {(data?.recent_activity || []).length === 0 ? (
            <div style={{ color: 'var(--text-tertiary)', fontSize: '0.82rem', textAlign: 'center', padding: 20 }}>
              No activity yet — launch a task to get started
            </div>
          ) : (
            data.recent_activity.slice(0, 10).map((msg, i) => (
              <div className="activity-item" key={i}>
                <div className={`activity-icon ${msg.message_type === 'alert' ? 'red' : msg.message_type === 'handoff' ? 'teal' : 'purple'}`}>
                  {msg.message_type === 'alert' ? '🚨' : msg.message_type === 'handoff' ? '🔄' : '📤'}
                </div>
                <div style={{ flex: 1 }}>
                  <div className="activity-text"><strong>{msg.from}</strong> → {msg.to}: {msg.notes || msg.message_type}</div>
                  <div className="activity-time">{new Date(msg.timestamp).toLocaleTimeString()}</div>
                </div>
              </div>
            ))
          )}
        </div>

        <div className="glass-card no-hover">
          <h3 style={{ marginBottom: 12, fontSize: '1rem', fontWeight: 700 }}>🧬 Agency Soul</h3>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
            <div><span style={{ color: 'var(--text-tertiary)', fontSize: '0.72rem' }}>Total Leads</span><div style={{ fontWeight: 700, fontSize: '1.2rem' }}>{soul.total_leads_processed || 0}</div></div>
            <div><span style={{ color: 'var(--text-tertiary)', fontSize: '0.72rem' }}>Total Emails</span><div style={{ fontWeight: 700, fontSize: '1.2rem' }}>{soul.total_emails_sent || 0}</div></div>
            <div><span style={{ color: 'var(--text-tertiary)', fontSize: '0.72rem' }}>Clients Won</span><div style={{ fontWeight: 700, fontSize: '1.2rem', color: 'var(--accent-success)' }}>{soul.total_clients_acquired || 0}</div></div>
            <div><span style={{ color: 'var(--text-tertiary)', fontSize: '0.72rem' }}>Learning Cycle</span><div style={{ fontWeight: 700, fontSize: '1.2rem' }}>{soul.learning_cycle || 1}</div></div>
            <div style={{ gridColumn: '1 / -1' }}><span style={{ color: 'var(--text-tertiary)', fontSize: '0.72rem' }}>Active Since</span><div style={{ fontWeight: 700, fontSize: '0.88rem', fontFamily: 'var(--font-mono)' }}>{soul.active_since || 'today'}</div></div>
          </div>
        </div>
      </div>
    </div>
  );
}
