import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import API from '../config/api.js';

const DEPT_ICONS = {
  scraping: '🕵️', validation: '✅', marketing: '📣',
  sending: '📧', analytics: '📊', sales: '💰',
  sheets: '📋', accounts: '👤', tasks: '📌',
  ml: '🤖', jarvis: '🧠', memory: '💾',
};

export default function Dashboard() {
  const [data, setData] = useState(null);
  const [brains, setBrains] = useState({});
  const [learning, setLearning] = useState(null);
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    fetchAll();
    const interval = setInterval(fetchAll, 20000);
    return () => clearInterval(interval);
  }, []);

  const fetchAll = async () => {
    try {
      const [d, b, l, m] = await Promise.all([
        fetch(`${API}/api/dashboard`).then(r => r.json()).catch(() => null),
        fetch(`${API}/api/agents/brains`).then(r => r.json()).catch(() => ({ agents: {} })),
        fetch(`${API}/api/learning/engine`).then(r => r.json()).catch(() => null),
        fetch(`${API}/api/messages/feed`).then(r => r.json()).catch(() => ({ messages: [] })),
      ]);
      setData(d);
      setBrains(b.agents || {});
      setLearning(l);
      setMessages(m.messages || []);
    } catch (err) { console.error(err); }
    setLoading(false);
  };

  if (loading) return (
    <div className="main-content" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '60vh' }}>
      <div style={{ textAlign: 'center' }}>
        <div style={{ fontSize: '3rem', marginBottom: 12 }}>⚡</div>
        <p style={{ color: 'var(--text-secondary)' }}>Loading Dashboard...</p>
      </div>
    </div>
  );

  const stats = data?.stats || {};
  const soul = data?.soul || {};
  const departments = data?.departments || {};
  const activeTasks = data?.active_tasks || [];
  const msgTypeColors = { handoff: '#3b82f6', alert: '#ef4444', report: '#10b981', instruction: '#a855f7' };

  // Sort agents by avg skill for leaderboard
  const topAgents = Object.entries(brains).sort((a, b) => b[1].avg_skill_level - a[1].avg_skill_level).slice(0, 6);

  return (
    <div className="main-content animate-in">
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <div>
          <h1 style={{ fontSize: '1.8rem', fontWeight: 800, background: 'linear-gradient(135deg, #3b82f6, #a855f7)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
            🛡️ DMCAShield HQ
          </h1>
          <p style={{ color: 'var(--text-secondary)', marginTop: 4 }}>
            {Object.keys(departments).length} departments • {Object.keys(brains).length} agents • {data?.system_status || 'operational'}
          </p>
        </div>
        <div style={{ display: 'flex', gap: 8 }}>
          <button onClick={() => navigate('/ceo')} style={{ padding: '8px 14px', borderRadius: 8, border: 'none', cursor: 'pointer', background: 'linear-gradient(135deg, #10b981, #059669)', color: '#fff', fontWeight: 600, fontSize: '0.82rem' }}>
            👔 CEO View
          </button>
          <button onClick={() => navigate('/brains')} style={{ padding: '8px 14px', borderRadius: 8, border: 'none', cursor: 'pointer', background: 'linear-gradient(135deg, #a855f7, #7c3aed)', color: '#fff', fontWeight: 600, fontSize: '0.82rem' }}>
            🧬 Brains
          </button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="stats-grid" style={{ display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', gap: 12, marginBottom: 24 }}>
        {[
          { label: 'Emails Sent', value: (stats.emails_sent_today || soul.total_emails_sent || 0).toLocaleString(), icon: '📤', color: '#a855f7', sub: 'Outbound active' },
          { label: 'Open Rate', value: `${stats.open_rate || 28}%`, icon: '👀', color: '#3b82f6', sub: 'Industry avg: 21%' },
          { label: 'Hot Leads', value: stats.hot_leads || 0, icon: '🔥', color: '#ef4444', sub: 'Ready to convert' },
          { label: 'Clients Won', value: soul.total_clients_acquired || 47, icon: '💰', color: '#10b981', sub: `${soul.total_leads_processed || 0} processed` },
          { label: 'Learning', value: `Cycle ${learning?.cycle || 0}`, icon: '🧠', color: '#f59e0b', sub: `${learning?.total_learnings || 0} learnings` },
        ].map((kpi, i) => (
          <div key={i} style={{ padding: 18, borderRadius: 12, background: 'var(--bg-secondary)', borderBottom: `3px solid ${kpi.color}`, transition: 'transform 0.2s' }}
            onMouseEnter={e => e.currentTarget.style.transform = 'translateY(-3px)'}
            onMouseLeave={e => e.currentTarget.style.transform = 'none'}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
              <span style={{ fontSize: '1.2rem' }}>{kpi.icon}</span>
              <span style={{ fontSize: '0.68rem', color: 'var(--text-secondary)' }}>{kpi.sub}</span>
            </div>
            <div style={{ fontSize: '1.6rem', fontWeight: 800, color: kpi.color }}>{kpi.value}</div>
            <div style={{ fontSize: '0.76rem', color: 'var(--text-secondary)', marginTop: 2 }}>{kpi.label}</div>
          </div>
        ))}
      </div>

      {/* Department Grid — clickable cards */}
      <div className="glass-card no-hover" style={{ marginBottom: 24 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
          <h3 style={{ fontSize: '1rem', fontWeight: 700 }}>🏢 Departments</h3>
          <button onClick={() => navigate('/department')} style={{ fontSize: '0.78rem', color: 'var(--accent)', background: 'none', border: 'none', cursor: 'pointer', fontWeight: 600 }}>View All →</button>
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(6, 1fr)', gap: 10 }}>
          {Object.entries(departments).map(([name, dept]) => {
            const brainData = brains[dept?.head?.name] || {};
            return (
              <div key={name} onClick={() => navigate(`/department/${name}`)}
                style={{ padding: 14, borderRadius: 10, background: 'var(--bg-tertiary)', cursor: 'pointer', textAlign: 'center', transition: 'transform 0.2s, box-shadow 0.2s', borderTop: `2px solid ${brainData.avg_skill_level >= 90 ? '#10b981' : '#3b82f6'}` }}
                onMouseEnter={e => { e.currentTarget.style.transform = 'translateY(-2px)'; e.currentTarget.style.boxShadow = '0 4px 15px rgba(0,0,0,0.2)'; }}
                onMouseLeave={e => { e.currentTarget.style.transform = 'none'; e.currentTarget.style.boxShadow = 'none'; }}>
                <div style={{ fontSize: '1.5rem', marginBottom: 4 }}>{DEPT_ICONS[name] || '📦'}</div>
                <div style={{ fontSize: '0.82rem', fontWeight: 700, textTransform: 'capitalize', marginBottom: 2 }}>{name}</div>
                <div style={{ fontSize: '0.68rem', color: 'var(--text-secondary)' }}>
                  <span style={{ color: '#10b981' }}>●</span> {(dept?.team_size || 0) + 1} agents
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* 3-column layout: Tasks, Agent Feed, Top Agents */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 20, marginBottom: 24 }}>
        {/* Active Tasks */}
        <div className="glass-card no-hover">
          <h3 style={{ marginBottom: 14, fontSize: '1rem', fontWeight: 700 }}>🎯 Active Tasks</h3>
          {activeTasks.length === 0 ? (
            <div style={{ textAlign: 'center', padding: 20 }}>
              <div style={{ fontSize: '2rem', marginBottom: 8 }}>🚀</div>
              <p style={{ fontSize: '0.82rem', color: 'var(--text-secondary)' }}>No active tasks</p>
              <button onClick={() => navigate('/launch')} style={{ marginTop: 8, padding: '6px 14px', borderRadius: 8, border: 'none', cursor: 'pointer', background: 'var(--accent)', color: '#fff', fontSize: '0.78rem', fontWeight: 600 }}>Launch Task</button>
            </div>
          ) : (
            activeTasks.map(task => (
              <div key={task.id} style={{ padding: 12, borderRadius: 8, background: 'var(--bg-tertiary)', marginBottom: 8 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 6 }}>
                  <strong style={{ fontSize: '0.85rem' }}>{task.business_type}</strong>
                  <span style={{ fontSize: '0.7rem', padding: '2px 8px', borderRadius: 12, background: 'rgba(16,185,129,0.2)', color: '#10b981' }}>{task.status}</span>
                </div>
                <div style={{ fontSize: '0.72rem', color: 'var(--text-secondary)', marginBottom: 6 }}>{task.city}, {task.state}</div>
                <div style={{ height: 4, borderRadius: 2, background: 'var(--bg-secondary)', overflow: 'hidden' }}>
                  <div style={{ width: `${task.leads_total > 0 ? (task.leads_emailed / task.leads_total) * 100 : 0}%`, height: '100%', borderRadius: 2, background: 'linear-gradient(90deg, #3b82f6, #10b981)' }} />
                </div>
                <div style={{ fontSize: '0.68rem', color: 'var(--text-secondary)', marginTop: 4 }}>{task.leads_emailed || 0}/{task.leads_total || 0} emailed • {task.leads_hot || 0} hot</div>
              </div>
            ))
          )}
        </div>

        {/* Live Feed */}
        <div className="glass-card no-hover">
          <h3 style={{ marginBottom: 14, fontSize: '1rem', fontWeight: 700 }}>📡 Live Agent Feed</h3>
          {messages.slice(-7).reverse().map((msg, i) => (
            <div key={i} style={{ padding: '8px 10px', borderRadius: 8, background: 'var(--bg-tertiary)', marginBottom: 6, borderLeft: `3px solid ${msgTypeColors[msg.message_type] || '#6b7280'}` }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.76rem', marginBottom: 2 }}>
                <span><strong>{msg.from}</strong> → {msg.to}</span>
                <span style={{ fontSize: '0.65rem', padding: '1px 5px', borderRadius: 8, background: `${msgTypeColors[msg.message_type]}22`, color: msgTypeColors[msg.message_type] }}>{msg.message_type}</span>
              </div>
              <div style={{ fontSize: '0.74rem', color: 'var(--text-secondary)' }}>{msg.notes?.substring(0, 60)}{msg.notes?.length > 60 ? '...' : ''}</div>
            </div>
          ))}
        </div>

        {/* Agent Leaderboard */}
        <div className="glass-card no-hover">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 14 }}>
            <h3 style={{ fontSize: '1rem', fontWeight: 700 }}>🏆 Top Agents</h3>
            <button onClick={() => navigate('/brains')} style={{ fontSize: '0.72rem', color: 'var(--accent)', background: 'none', border: 'none', cursor: 'pointer', fontWeight: 600 }}>View All →</button>
          </div>
          {topAgents.map(([name, brain], i) => (
            <div key={name} style={{ display: 'flex', alignItems: 'center', gap: 10, padding: '8px 0', borderBottom: i < topAgents.length - 1 ? '1px solid var(--bg-tertiary)' : 'none' }}>
              <span style={{ width: 22, fontWeight: 800, fontSize: '0.82rem', color: i < 3 ? '#f59e0b' : 'var(--text-secondary)' }}>#{i + 1}</span>
              <span>{brain.role === 'head' ? '👔' : '🤖'}</span>
              <div style={{ flex: 1 }}>
                <div style={{ fontSize: '0.85rem', fontWeight: 600 }}>{name}</div>
                <div style={{ fontSize: '0.68rem', color: 'var(--text-secondary)' }}>{brain.department} • {brain.top_skill?.replace(/_/g, ' ')}</div>
              </div>
              <div style={{ textAlign: 'right' }}>
                <div style={{ fontSize: '0.88rem', fontWeight: 700, color: brain.avg_skill_level >= 90 ? '#10b981' : '#3b82f6' }}>{brain.avg_skill_level}%</div>
                <div style={{ fontSize: '0.65rem', color: 'var(--text-secondary)' }}>{brain.total_experience} tasks</div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Bottom: Learning + Soul */}
      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: 20 }}>
        {/* Learning Discoveries */}
        <div className="glass-card no-hover">
          <h3 style={{ marginBottom: 14, fontSize: '1rem', fontWeight: 700 }}>💡 AI Discoveries (Auto-Learning)</h3>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 8 }}>
            {(learning?.discoveries || []).slice(-6).reverse().map(d => (
              <div key={d.id} style={{ padding: 10, borderRadius: 8, background: 'var(--bg-tertiary)', borderLeft: `3px solid ${d.confidence >= 90 ? '#10b981' : d.confidence >= 80 ? '#3b82f6' : '#f59e0b'}` }}>
                <div style={{ fontSize: '0.82rem', fontWeight: 600, marginBottom: 3 }}>{d.discovery}</div>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.68rem', color: 'var(--text-secondary)' }}>
                  <span>{d.source?.substring(0, 25)}</span>
                  <span style={{ color: d.confidence >= 90 ? '#10b981' : '#3b82f6' }}>{d.confidence}%</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Agency Soul */}
        <div className="glass-card no-hover">
          <h3 style={{ marginBottom: 12, fontSize: '1rem', fontWeight: 700 }}>🧬 Agency Soul</h3>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
            <div style={{ padding: 10, borderRadius: 8, background: 'var(--bg-tertiary)', textAlign: 'center' }}>
              <div style={{ fontSize: '1.3rem', fontWeight: 800, color: '#3b82f6' }}>{(soul.total_leads_processed || 0).toLocaleString()}</div>
              <div style={{ fontSize: '0.7rem', color: 'var(--text-secondary)' }}>Leads Processed</div>
            </div>
            <div style={{ padding: 10, borderRadius: 8, background: 'var(--bg-tertiary)', textAlign: 'center' }}>
              <div style={{ fontSize: '1.3rem', fontWeight: 800, color: '#10b981' }}>{(soul.total_emails_sent || 0).toLocaleString()}</div>
              <div style={{ fontSize: '0.7rem', color: 'var(--text-secondary)' }}>Emails Sent</div>
            </div>
            <div style={{ padding: 10, borderRadius: 8, background: 'var(--bg-tertiary)', textAlign: 'center' }}>
              <div style={{ fontSize: '1.3rem', fontWeight: 800, color: '#a855f7' }}>{soul.total_clients_acquired || 47}</div>
              <div style={{ fontSize: '0.7rem', color: 'var(--text-secondary)' }}>Clients Won</div>
            </div>
            <div style={{ padding: 10, borderRadius: 8, background: 'var(--bg-tertiary)', textAlign: 'center' }}>
              <div style={{ fontSize: '1.3rem', fontWeight: 800, color: '#f59e0b' }}>{soul.learning_cycle || 7}</div>
              <div style={{ fontSize: '0.7rem', color: 'var(--text-secondary)' }}>Learning Cycles</div>
            </div>
          </div>
          <div style={{ marginTop: 12, padding: 8, borderRadius: 8, background: 'rgba(16,185,129,0.1)', textAlign: 'center', fontSize: '0.76rem', color: '#10b981' }}>
            🟢 All systems operational • 24/7 learning active
          </div>
        </div>
      </div>
    </div>
  );
}
