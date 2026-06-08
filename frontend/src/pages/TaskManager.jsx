import { useState, useEffect } from 'react';
import API from '../config/api.js';

export default function TaskManager() {
  const [tasks, setTasks] = useState([]);
  const [dripStatus, setDripStatus] = useState(null);
  const [sendingBatch, setSendingBatch] = useState(false);
  const [batchResult, setBatchResult] = useState('');

  const refreshData = async () => {
    try {
      const tasksRes = await fetch(`${API}/api/tasks`);
      setTasks(await tasksRes.json());
      
      const dripRes = await fetch(`${API}/api/drip/status`);
      setDripStatus(await dripRes.json());
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    refreshData();
    const interval = setInterval(refreshData, 15000); // Poll every 15s for status updates
    return () => clearInterval(interval);
  }, []);

  const handleAction = async (id, action) => {
    await fetch(`${API}/api/tasks/${id}/${action}`, { method: 'POST' });
    refreshData();
  };

  const triggerDripSend = async () => {
    setSendingBatch(true);
    setBatchResult('Initiating SMTP connection, warming up templates...');
    try {
      const res = await fetch(`${API}/api/drip/send`, { method: 'POST' });
      const data = await res.json();
      if (data.error) {
        setBatchResult(`❌ Error: ${data.error}`);
      } else if (data.smtp_error) {
        setBatchResult(`❌ SMTP Connection Failed: ${data.smtp_error}`);
      } else {
        const sentDetails = data.details
          ? data.details.filter(d => d.status === 'sent').map(d => d.lead).join(', ')
          : '';
        setBatchResult(`✅ ${data.message} ${sentDetails ? `(Leads: ${sentDetails})` : ''}`);
      }
      refreshData();
    } catch (err) {
      setBatchResult('❌ Failed to trigger drip campaign.');
    }
    setSendingBatch(false);
  };

  const phaseIcon = (status) => status === 'complete' ? '✅' : status === 'in_progress' ? '🔄' : status === 'active' ? '🟢' : '⏳';

  return (
    <div className="main-content animate-in">
      <div className="page-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 16 }}>
        <div>
          <h1>📋 Task Manager</h1>
          <p>Track, pause, and manage all outreach campaigns</p>
        </div>
        
        {/* Drip Telemetry Card */}
        {dripStatus && !dripStatus.error && (
          <div style={{ display: 'flex', gap: 12, background: 'var(--bg-secondary)', padding: '10px 16px', borderRadius: 12, border: '1px solid var(--border-subtle)', alignItems: 'center' }}>
            <div style={{ fontSize: '0.8rem', textAlign: 'right' }}>
              <div style={{ fontWeight: 600 }}>📧 Outbound Queue: <span style={{ color: 'var(--accent)' }}>{dripStatus.queued || 0} queued</span></div>
              <div style={{ fontSize: '0.7rem', color: 'var(--text-tertiary)', marginTop: 2 }}>
                Warmup: <span style={{ textTransform: 'capitalize', color: 'var(--accent-secondary)' }}>{dripStatus.warmup_phase || 'unknown'}</span> • Sent Today: {dripStatus.sent_today || 0}/{dripStatus.daily_limit || 3}
              </div>
            </div>
            <button 
              className="btn btn-primary" 
              style={{ padding: '8px 14px', fontSize: '0.78rem', display: 'flex', alignItems: 'center', gap: 4, height: 'fit-content' }}
              disabled={sendingBatch}
              onClick={triggerDripSend}
            >
              {sendingBatch ? '⏳ Sending...' : '🚀 Send Batch'}
            </button>
          </div>
        )}
      </div>

      {batchResult && (
        <div style={{ 
          padding: 12, 
          borderRadius: 8, 
          background: batchResult.includes('❌') ? 'rgba(239, 68, 68, 0.15)' : 'rgba(16, 185, 129, 0.15)', 
          borderLeft: `4px solid ${batchResult.includes('❌') ? '#ef4444' : '#10b981'}`,
          fontSize: '0.82rem',
          marginBottom: 16,
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          animation: 'fadeIn 0.3s'
        }}>
          <span>{batchResult}</span>
          <button style={{ background: 'none', border: 'none', color: 'var(--text-secondary)', cursor: 'pointer', fontSize: '0.85rem', padding: '0 8px' }} onClick={() => setBatchResult('')}>✕</button>
        </div>
      )}

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
