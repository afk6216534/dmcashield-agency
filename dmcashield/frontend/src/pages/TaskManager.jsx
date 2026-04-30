import { useState, useEffect } from 'react';
const API = 'http://localhost:8000';

export default function TaskManager() {
  const [tasks, setTasks] = useState([]);
  useEffect(() => { fetch(`${API}/api/tasks`).then(r => r.json()).then(setTasks).catch(console.error); }, []);

  const handleAction = async (id, action) => {
    await fetch(`${API}/api/tasks/${id}/${action}`, { method: 'POST' });
    const res = await fetch(`${API}/api/tasks`);
    setTasks(await res.json());
  };

  const phaseIcon = (status) => status === 'complete' ? '✅' : status === 'in_progress' ? '🔄' : status === 'active' ? '🟢' : '⏳';

  return (
    <div className="main-content animate-in">
      <div className="page-header">
        <h1>📋 Task Manager</h1>
        <p>Track, pause, and manage all outreach campaigns</p>
      </div>

      {tasks.length === 0 ? (
        <div className="glass-card no-hover"><div className="empty-state"><div className="empty-icon">📋</div><h3>No tasks created yet</h3><p style={{ color: 'var(--text-tertiary)' }}>Go to Launch Task to create your first campaign</p></div></div>
      ) : (
        tasks.map(task => (
          <div className="glass-card" key={task.id} style={{ marginBottom: 16 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
              <div>
                <h3 style={{ fontSize: '1.1rem', fontWeight: 700 }}>
                  {task.business_type.charAt(0).toUpperCase() + task.business_type.slice(1)} — {task.city}, {task.state}
                </h3>
                <div style={{ fontSize: '0.72rem', color: 'var(--text-tertiary)', fontFamily: 'var(--font-mono)' }}>ID: {task.id?.slice(0, 8)} • Created: {task.created_at ? new Date(task.created_at).toLocaleDateString() : 'N/A'}</div>
              </div>
              <div style={{ display: 'flex', gap: 8 }}>
                <span className={`badge badge-${task.status}`}>{task.status}</span>
                {task.status === 'active' && <button className="btn btn-secondary" style={{ padding: '4px 12px', fontSize: '0.72rem' }} onClick={() => handleAction(task.id, 'pause')}>⏸ Pause</button>}
                {task.status === 'paused' && <button className="btn btn-success" style={{ padding: '4px 12px', fontSize: '0.72rem' }} onClick={() => handleAction(task.id, 'resume')}>▶ Resume</button>}
              </div>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(6, 1fr)', gap: 8, marginBottom: 12 }}>
              {[
                { label: 'Scraping', key: 'phase_scraping' },
                { label: 'Validation', key: 'phase_validation' },
                { label: 'Funnels', key: 'phase_funnel_creation' },
                { label: 'Sending', key: 'phase_email_sending' },
                { label: 'Tracking', key: 'phase_tracking' },
                { label: 'Sales', key: 'phase_sales' },
              ].map(p => (
                <div key={p.key} style={{ textAlign: 'center', padding: 8, background: 'var(--bg-input)', borderRadius: 'var(--radius-sm)', fontSize: '0.72rem' }}>
                  <div>{phaseIcon(task[p.key] || 'pending')}</div>
                  <div style={{ color: 'var(--text-secondary)', marginTop: 2 }}>{p.label}</div>
                </div>
              ))}
            </div>

            <div className="progress-bar"><div className="progress-fill" style={{ width: `${task.leads_total > 0 ? (task.leads_emailed / task.leads_total) * 100 : 5}%` }} /></div>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.72rem', color: 'var(--text-tertiary)', marginTop: 6 }}>
              <span>📊 {task.leads_total} leads</span>
              <span>📤 {task.leads_emailed} emailed</span>
              <span>👀 {task.leads_opened} opened</span>
              <span>💬 {task.leads_replied} replied</span>
              <span>🔥 {task.leads_hot} hot</span>
              <span>📈 {task.open_rate}% open rate</span>
            </div>
          </div>
        ))
      )}
    </div>
  );
}
