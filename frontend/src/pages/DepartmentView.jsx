import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';

import API from '../config/api.js';

const DEPT_LIST = [
  { key: 'scraping', icon: '🕵️', name: 'Scraping' },
  { key: 'validation', icon: '✅', name: 'Validation' },
  { key: 'marketing', icon: '📣', name: 'Marketing' },
  { key: 'sending', icon: '📧', name: 'Sending' },
  { key: 'analytics', icon: '📊', name: 'Analytics' },
  { key: 'sales', icon: '💰', name: 'Sales' },
  { key: 'accounts', icon: '👤', name: 'Accounts' },
  { key: 'tasks', icon: '📌', name: 'Tasks' },
  { key: 'ml', icon: '🤖', name: 'ML' },
  { key: 'jarvis', icon: '🧠', name: 'JARVIS' },
  { key: 'memory', icon: '💾', name: 'Memory' },
  { key: 'sheets', icon: '📋', name: 'Sheets' },
];

export default function DepartmentView() {
  const { dept } = useParams();
  const [data, setData] = useState(null);
  const [chatInput, setChatInput] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [chatLoading, setChatLoading] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (dept) loadDepartment(dept);
  }, [dept]);

  const loadDepartment = async (name) => {
    setLoading(true);
    try {
      const r = await fetch(`${API}/api/departments/${name}`);
      const d = await r.json();
      setData(d);
    } catch (e) { console.error(e); }
    setLoading(false);
  };

  const sendChat = async (e) => {
    e.preventDefault();
    if (!chatInput.trim()) return;
    const msg = chatInput;
    setChatHistory(h => [...h, { role: 'user', text: msg, time: new Date().toLocaleTimeString() }]);
    setChatInput('');
    setChatLoading(true);
    try {
      const r = await fetch(`${API}/api/departments/${dept}/chat`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: msg })
      });
      const d = await r.json();
      setChatHistory(h => [...h, { role: 'agent', text: d.response, agent: d.agent, time: new Date().toLocaleTimeString() }]);
    } catch {
      setChatHistory(h => [...h, { role: 'agent', text: 'Connection error — backend may be offline.', time: new Date().toLocaleTimeString() }]);
    }
    setChatLoading(false);
  };

  if (!dept) {
    return (
      <main className="main-content">
        <div className="page-header">
          <h1>🏢 Departments</h1>
          <p className="text-secondary">Click a department to see its full details and chat with the head agent</p>
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: '1rem' }}>
          {DEPT_LIST.map(d => (
            <Link key={d.key} to={`/department/${d.key}`} style={{ textDecoration: 'none' }}>
              <div className="card" style={{ textAlign: 'center', padding: '2rem', cursor: 'pointer', transition: 'transform 0.2s' }}
                onMouseEnter={e => e.currentTarget.style.transform = 'scale(1.03)'}
                onMouseLeave={e => e.currentTarget.style.transform = 'scale(1)'}>
                <div style={{ fontSize: '3rem', marginBottom: '0.5rem' }}>{d.icon}</div>
                <div style={{ fontWeight: 700, fontSize: '1.1rem' }}>{d.name}</div>
                <div className="text-secondary" style={{ fontSize: '0.8rem', marginTop: '0.25rem' }}>Click to deep-dive →</div>
              </div>
            </Link>
          ))}
        </div>
      </main>
    );
  }

  if (loading) {
    return (
      <main className="main-content" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
        <div style={{ textAlign: 'center' }}>
          <div style={{ fontSize: '3rem', animation: 'spin 1s linear infinite' }}>⏳</div>
          <p className="text-secondary">Loading {dept}...</p>
        </div>
      </main>
    );
  }

  if (!data) {
    return <main className="main-content"><p>Department not found.</p></main>;
  }

  return (
    <main className="main-content">
      {/* Header */}
      <div className="page-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h1>{data.icon} {data.title}</h1>
          <p className="text-secondary">{data.description}</p>
        </div>
        <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
          <span style={{ width: 10, height: 10, borderRadius: '50%', background: 'var(--success)', boxShadow: '0 0 8px var(--success)' }}></span>
          <span style={{ color: 'var(--success)', fontWeight: 600 }}>{data.status}</span>
          <span className="text-secondary" style={{ marginLeft: '0.5rem' }}>• {data.team_size} agents</span>
        </div>
      </div>

      {/* Pipeline */}
      <div className="card" style={{ marginBottom: '1.5rem' }}>
        <h2 style={{ marginBottom: '1rem' }}>⚙️ Process Pipeline</h2>
        <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center', overflowX: 'auto', padding: '0.5rem 0' }}>
          {data.pipeline?.map((step, i) => (
            <div key={i} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <div style={{
                background: 'rgba(139, 92, 246, 0.15)', border: '1px solid rgba(139, 92, 246, 0.3)',
                borderRadius: '12px', padding: '0.75rem 1.25rem', whiteSpace: 'nowrap',
                fontWeight: 600, fontSize: '0.9rem', textAlign: 'center', minWidth: '120px'
              }}>
                <div style={{ fontSize: '0.7rem', color: 'var(--text-secondary)', marginBottom: '0.2rem' }}>Step {i + 1}</div>
                {step}
              </div>
              {i < data.pipeline.length - 1 && <span style={{ color: 'var(--primary)', fontSize: '1.2rem' }}>→</span>}
            </div>
          ))}
        </div>
      </div>

      {/* Funnel (Marketing only) */}
      {data.funnel && (
        <div className="card" style={{ marginBottom: '1.5rem' }}>
          <h2 style={{ marginBottom: '1rem' }}>🎯 Email Funnel Sequence</h2>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', gap: '0.75rem' }}>
            {data.funnel.map((f, i) => (
              <div key={i} className="card" style={{
                textAlign: 'center', padding: '1rem',
                background: `rgba(139, 92, 246, ${0.05 + i * 0.04})`,
                borderLeft: `3px solid hsl(${260 - i * 20}, 70%, 60%)`
              }}>
                <div style={{ fontSize: '1.5rem', fontWeight: 700, color: 'var(--primary)' }}>#{f.step}</div>
                <div style={{ fontWeight: 600, marginTop: '0.25rem' }}>{f.name}</div>
                <div className="text-secondary" style={{ fontSize: '0.8rem', margin: '0.25rem 0' }}>{f.goal}</div>
                <div style={{ fontSize: '0.75rem', color: 'var(--primary)' }}>{f.timing}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Techniques + KPIs side by side */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem', marginBottom: '1.5rem' }}>
        <div className="card">
          <h2 style={{ marginBottom: '1rem' }}>🛠 Techniques</h2>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
            {data.techniques?.map((t, i) => (
              <div key={i} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', padding: '0.5rem', background: 'rgba(255,255,255,0.03)', borderRadius: '8px' }}>
                <span style={{ color: 'var(--success)' }}>✦</span>
                <span>{t}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="card">
          <h2 style={{ marginBottom: '1rem' }}>📊 Live KPIs</h2>
          {data.kpis && Object.entries(data.kpis).map(([key, val]) => (
            <div key={key} style={{ display: 'flex', justifyContent: 'space-between', padding: '0.75rem', background: 'rgba(255,255,255,0.03)', borderRadius: '8px', marginBottom: '0.5rem' }}>
              <span className="text-secondary" style={{ textTransform: 'capitalize' }}>{key.replace(/_/g, ' ')}</span>
              <span style={{ fontWeight: 700, fontSize: '1.1rem', color: 'var(--primary)' }}>{typeof val === 'number' ? val.toLocaleString() : val}</span>
            </div>
          ))}
          {(!data.kpis || Object.keys(data.kpis).length === 0) && (
            <p className="text-secondary">No KPI data yet — launch a task to generate data</p>
          )}
        </div>
      </div>

      {/* Agents */}
      <div className="card" style={{ marginBottom: '1.5rem' }}>
        <h2 style={{ marginBottom: '1rem' }}>👥 Team ({data.team_size} agents)</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: '0.75rem' }}>
          {data.head?.name && (
            <div className="card" style={{ padding: '1rem', borderLeft: '3px solid var(--warning)' }}>
              <div style={{ fontWeight: 700 }}>{data.head.name}</div>
              <div className="text-secondary" style={{ fontSize: '0.8rem' }}>HEAD — {data.head.status}</div>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', marginTop: '0.25rem' }}>
                Tasks: {data.head.tasks_completed || 0} • Brain: {data.head.brain_size || 0}
              </div>
            </div>
          )}
          {data.team?.map((a, i) => (
            <div key={i} className="card" style={{ padding: '1rem', borderLeft: '3px solid var(--primary)' }}>
              <div style={{ fontWeight: 700 }}>{a.name}</div>
              <div className="text-secondary" style={{ fontSize: '0.8rem' }}>{a.role} — {a.status}</div>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', marginTop: '0.25rem' }}>
                Tasks: {a.tasks_completed || 0} • Brain: {a.brain_size || 0}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Chat with Department Head */}
      <div className="card">
        <h2 style={{ marginBottom: '1rem' }}>💬 Chat with {data.head?.name || dept + ' Head'}</h2>
        <div style={{ maxHeight: '300px', overflowY: 'auto', marginBottom: '1rem', padding: '0.5rem' }}>
          {chatHistory.length === 0 && (
            <p className="text-secondary" style={{ textAlign: 'center', padding: '2rem' }}>
              Start a conversation — ask about pipeline, techniques, stats, or give instructions
            </p>
          )}
          {chatHistory.map((m, i) => (
            <div key={i} style={{
              display: 'flex', justifyContent: m.role === 'user' ? 'flex-end' : 'flex-start',
              marginBottom: '0.75rem'
            }}>
              <div style={{
                maxWidth: '70%', padding: '0.75rem 1rem', borderRadius: '12px',
                background: m.role === 'user' ? 'var(--primary)' : 'rgba(255,255,255,0.06)',
                color: m.role === 'user' ? '#fff' : 'var(--text-primary)'
              }}>
                {m.agent && <div style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--warning)', marginBottom: '0.25rem' }}>{m.agent}</div>}
                <div style={{ whiteSpace: 'pre-wrap', fontSize: '0.9rem' }}>{m.text}</div>
                <div style={{ fontSize: '0.7rem', color: 'rgba(255,255,255,0.5)', marginTop: '0.3rem' }}>{m.time}</div>
              </div>
            </div>
          ))}
        </div>
        <form onSubmit={sendChat} style={{ display: 'flex', gap: '0.75rem' }}>
          <input className="jarvis-input" value={chatInput} onChange={e => setChatInput(e.target.value)}
            placeholder={`Talk to ${data.head?.name || dept}... (try "show pipeline" or "change strategy")`}
            disabled={chatLoading} style={{ flex: 1 }} />
          <button className="btn btn-primary" type="submit" disabled={chatLoading}>
            {chatLoading ? '...' : 'Send'}
          </button>
        </form>
      </div>
    </main>
  );
}
