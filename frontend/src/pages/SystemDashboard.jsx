import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import API from '../config/api.js';

export default function SystemDashboard() {
  const [status, setStatus] = useState(null);
  const [brains, setBrains] = useState({});
  const [learning, setLearning] = useState(null);
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [lastUpdate, setLastUpdate] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 30000);
    return () => clearInterval(interval);
  }, []);

  const loadData = async () => {
    setLoading(true);
    setLastUpdate(new Date().toLocaleTimeString());
    try {
      const [s, b, l, m] = await Promise.all([
        fetch(`${API}/api/ceo/overview`).then(r => r.json()).catch(() => null),
        fetch(`${API}/api/agents/brains`).then(r => r.json()).catch(() => ({ agents: {} })),
        fetch(`${API}/api/learning/engine`).then(r => r.json()).catch(() => null),
        fetch(`${API}/api/messages/feed`).then(r => r.json()).catch(() => ({ messages: [] })),
      ]);
      setStatus(s);
      setBrains(b.agents || {});
      setLearning(l);
      setMessages(m.messages || []);
    } catch (e) { console.error(e); }
    setLoading(false);
  };

  const deptIcons = { scraping: '🕵️', validation: '✅', marketing: '📣', sending: '📧', analytics: '📊', sales: '💰', accounts: '👤', tasks: '📌', ml: '🤖', jarvis: '🧠', memory: '💾', sheets: '📋' };
  const msgTypeColors = { handoff: '#3b82f6', alert: '#ef4444', report: '#10b981', instruction: '#a855f7' };

  if (loading && !status) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '60vh' }}>
        <div style={{ textAlign: 'center' }}>
          <div style={{ fontSize: '3rem', marginBottom: 12, animation: 'spin 1s linear infinite' }}>⏳</div>
          <p style={{ color: 'var(--text-secondary)' }}>Loading Control Tower...</p>
        </div>
      </div>
    );
  }

  const deptStatuses = status?.department_statuses || {};
  const soul = status?.soul || {};

  return (
    <div style={{ padding: 24 }}>
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <div>
          <h1 style={{ fontSize: '1.8rem', fontWeight: 800, background: 'linear-gradient(135deg, #3b82f6, #10b981)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>🏢 Control Tower</h1>
          <p style={{ color: 'var(--text-secondary)', marginTop: 4 }}>12 Departments • 36 Agents • Real-Time Monitoring</p>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <span style={{ fontSize: '0.78rem', color: 'var(--text-secondary)' }}>{lastUpdate ? `🕐 ${lastUpdate}` : ''}</span>
          <button onClick={loadData} style={{ padding: '8px 16px', borderRadius: 8, border: 'none', cursor: 'pointer', background: 'var(--accent)', color: '#fff', fontWeight: 600, fontSize: '0.85rem' }}>🔄 Refresh</button>
        </div>
      </div>

      {/* Status banner */}
      <div style={{ padding: 16, borderRadius: 12, marginBottom: 24, background: status ? 'rgba(16,185,129,0.1)' : 'rgba(245,158,11,0.1)', border: `1px solid ${status ? 'rgba(16,185,129,0.3)' : 'rgba(245,158,11,0.3)'}`, display: 'flex', alignItems: 'center', gap: 12 }}>
        <span style={{ width: 12, height: 12, borderRadius: '50%', background: status ? '#10b981' : '#f59e0b', display: 'inline-block', animation: 'pulse 2s infinite' }}></span>
        <span style={{ fontWeight: 700, color: status ? '#10b981' : '#f59e0b' }}>{status ? '✅ LIVE — Connected to Vercel Backend' : '⚠️ Connecting...'}</span>
      </div>

      {/* Company KPIs */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', gap: 12, marginBottom: 24 }}>
        {[
          { label: 'Leads Processed', value: soul.total_leads_processed || 0, color: '#3b82f6', icon: '👥' },
          { label: 'Emails Sent', value: (soul.total_emails_sent || 0).toLocaleString(), color: '#10b981', icon: '📧' },
          { label: 'Clients Acquired', value: soul.total_clients_acquired || 0, color: '#a855f7', icon: '💰' },
          { label: 'Learning Cycle', value: soul.learning_cycle || 0, color: '#f59e0b', icon: '🧠' },
          { label: 'Active Tasks', value: status?.active_tasks || 0, color: '#ef4444', icon: '📋' },
        ].map((kpi, i) => (
          <div key={i} style={{ padding: 18, borderRadius: 12, background: 'var(--bg-secondary)', textAlign: 'center', borderBottom: `3px solid ${kpi.color}` }}>
            <div style={{ fontSize: '1.6rem', marginBottom: 4 }}>{kpi.icon}</div>
            <div style={{ fontSize: '1.5rem', fontWeight: 800, color: kpi.color }}>{kpi.value}</div>
            <div style={{ fontSize: '0.76rem', color: 'var(--text-secondary)' }}>{kpi.label}</div>
          </div>
        ))}
      </div>

      {/* Departments Grid — 12 departments with agents */}
      <h2 style={{ fontSize: '1.2rem', fontWeight: 700, marginBottom: 12 }}>🏢 All Departments ({Object.keys(deptStatuses).length})</h2>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 12, marginBottom: 24 }}>
        {Object.entries(deptStatuses).map(([name, data]) => {
          const head = data?.head || {};
          const team = data?.team || [];
          const agentBrainData = brains[head.name] || {};
          return (
            <div key={name} onClick={() => navigate(`/department/${name}`)} style={{ padding: 16, borderRadius: 12, background: 'var(--bg-secondary)', cursor: 'pointer', transition: 'transform 0.2s, box-shadow 0.2s', borderLeft: `3px solid ${head.status === 'active' ? '#10b981' : '#ef4444'}` }}
              onMouseEnter={e => { e.currentTarget.style.transform = 'translateY(-2px)'; e.currentTarget.style.boxShadow = '0 4px 20px rgba(0,0,0,0.3)'; }}
              onMouseLeave={e => { e.currentTarget.style.transform = 'none'; e.currentTarget.style.boxShadow = 'none'; }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
                <span style={{ fontSize: '1.4rem' }}>{deptIcons[name] || '📦'}</span>
                <span style={{ fontSize: '0.72rem', padding: '2px 8px', borderRadius: 12, background: 'rgba(16,185,129,0.2)', color: '#10b981' }}>ONLINE</span>
              </div>
              <div style={{ fontWeight: 700, fontSize: '0.92rem', marginBottom: 4, textTransform: 'capitalize' }}>{name}</div>
              <div style={{ fontSize: '0.78rem', color: 'var(--text-secondary)', marginBottom: 6 }}>
                👔 {head.name || 'N/A'} + {team.length} agent{team.length !== 1 ? 's' : ''}
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.72rem', color: 'var(--text-secondary)' }}>
                <span>Tasks: {head.tasks_completed || 0}</span>
                <span>Avg: {agentBrainData.avg_skill_level || '—'}%</span>
              </div>
            </div>
          );
        })}
      </div>

      {/* Bottom grid: Agent Rankings + Message Feed + Learning */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 20 }}>
        {/* Top Agents */}
        <div style={{ background: 'var(--bg-secondary)', borderRadius: 12, padding: 20 }}>
          <h3 style={{ fontSize: '1rem', fontWeight: 700, marginBottom: 14 }}>🏆 Top Agents by Skill</h3>
          {Object.entries(brains).sort((a, b) => b[1].avg_skill_level - a[1].avg_skill_level).slice(0, 8).map(([name, brain], i) => (
            <div key={name} style={{ display: 'flex', alignItems: 'center', gap: 10, padding: '7px 0', borderBottom: i < 7 ? '1px solid var(--bg-tertiary)' : 'none' }}>
              <span style={{ width: 20, fontWeight: 800, fontSize: '0.82rem', color: i < 3 ? '#f59e0b' : 'var(--text-secondary)' }}>#{i + 1}</span>
              <span style={{ fontSize: '0.82rem' }}>{brain.role === 'head' ? '👔' : '🤖'}</span>
              <span style={{ flex: 1, fontSize: '0.85rem', fontWeight: 600 }}>{name}</span>
              <span style={{ fontSize: '0.78rem', fontWeight: 700, color: brain.avg_skill_level >= 90 ? '#10b981' : '#3b82f6' }}>{brain.avg_skill_level}%</span>
            </div>
          ))}
        </div>

        {/* Message Feed */}
        <div style={{ background: 'var(--bg-secondary)', borderRadius: 12, padding: 20 }}>
          <h3 style={{ fontSize: '1rem', fontWeight: 700, marginBottom: 14 }}>💬 Agent Communications</h3>
          {messages.slice(-8).reverse().map((msg, i) => (
            <div key={i} style={{ padding: '8px 10px', borderRadius: 8, background: 'var(--bg-tertiary)', marginBottom: 6, borderLeft: `3px solid ${msgTypeColors[msg.message_type] || '#6b7280'}` }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.78rem', marginBottom: 3 }}>
                <span><strong>{msg.from}</strong> → <strong>{msg.to}</strong></span>
                <span style={{ padding: '1px 6px', borderRadius: 8, fontSize: '0.68rem', background: `${msgTypeColors[msg.message_type] || '#6b7280'}22`, color: msgTypeColors[msg.message_type] || '#6b7280' }}>{msg.message_type}</span>
              </div>
              <div style={{ fontSize: '0.78rem', color: 'var(--text-secondary)' }}>{msg.notes}</div>
            </div>
          ))}
        </div>

        {/* Learning Status */}
        <div style={{ background: 'var(--bg-secondary)', borderRadius: 12, padding: 20 }}>
          <h3 style={{ fontSize: '1rem', fontWeight: 700, marginBottom: 14 }}>📚 Auto-Learning Engine</h3>
          {learning && (
            <>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 8, marginBottom: 14 }}>
                <div style={{ padding: 10, borderRadius: 8, background: 'var(--bg-tertiary)', textAlign: 'center' }}>
                  <div style={{ fontSize: '1.3rem', fontWeight: 800, color: '#10b981' }}>🟢</div>
                  <div style={{ fontSize: '0.72rem', color: 'var(--text-secondary)' }}>ACTIVE 24/7</div>
                </div>
                <div style={{ padding: 10, borderRadius: 8, background: 'var(--bg-tertiary)', textAlign: 'center' }}>
                  <div style={{ fontSize: '1.3rem', fontWeight: 800, color: '#3b82f6' }}>{learning.cycle}</div>
                  <div style={{ fontSize: '0.72rem', color: 'var(--text-secondary)' }}>Cycles</div>
                </div>
              </div>
              <div style={{ fontSize: '0.82rem', fontWeight: 600, marginBottom: 8 }}>Latest Discoveries:</div>
              {(learning.discoveries || []).slice(-4).reverse().map(d => (
                <div key={d.id} style={{ padding: '6px 10px', borderRadius: 6, background: 'var(--bg-tertiary)', marginBottom: 4, fontSize: '0.76rem' }}>
                  <span style={{ color: '#10b981', marginRight: 4 }}>✓</span> {d.discovery.substring(0, 60)}{d.discovery.length > 60 ? '...' : ''}
                </div>
              ))}
              <button onClick={() => navigate('/brains')} style={{ marginTop: 10, width: '100%', padding: '8px 0', borderRadius: 8, border: 'none', cursor: 'pointer', background: 'linear-gradient(135deg, #a855f7, #6366f1)', color: '#fff', fontWeight: 600, fontSize: '0.82rem' }}>
                🧬 View Agent Brains →
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  );
}