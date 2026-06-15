import { useState, useEffect } from 'react';
import API from '../config/api.js';

export default function TaskManager() {
  const [tasks, setTasks] = useState([]);
  const [dripStatus, setDripStatus] = useState(null);
  const [sendingBatch, setSendingBatch] = useState(false);
  const [batchResult, setBatchResult] = useState('');
  
  // Lead review modal state
  const [reviewingTask, setReviewingTask] = useState(null);
  const [taskLeads, setTaskLeads] = useState([]);
  const [leadStats, setLeadStats] = useState({});
  const [loadingLeads, setLoadingLeads] = useState(false);
  const [approving, setApproving] = useState(false);
  const [approveResult, setApproveResult] = useState('');

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
    const interval = setInterval(refreshData, 15000);
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

  // ── Review Leads for a task ──
  const reviewLeads = async (taskId) => {
    setLoadingLeads(true);
    setReviewingTask(taskId);
    setTaskLeads([]);
    setApproveResult('');
    try {
      const res = await fetch(`${API}/api/tasks/${taskId}/leads`);
      const data = await res.json();
      setTaskLeads(data.leads || []);
      setLeadStats({ total: data.total, with_email: data.with_email, without_email: data.without_email });
    } catch (err) {
      console.error('Failed to load leads:', err);
      setTaskLeads([]);
    }
    setLoadingLeads(false);
  };

  // ── Approve task and start outreach ──
  const approveTask = async (taskId) => {
    setApproving(true);
    setApproveResult('');
    try {
      const res = await fetch(`${API}/api/tasks/${taskId}/approve`, { method: 'POST' });
      const data = await res.json();
      if (data.error || data.detail) {
        setApproveResult(`❌ ${data.error || data.detail}`);
      } else {
        setApproveResult(`✅ ${data.message}`);
        setReviewingTask(null);
        refreshData();
      }
    } catch (err) {
      setApproveResult('❌ Failed to approve task.');
    }
    setApproving(false);
  };

  const phaseIcon = (status) => {
    if (status === 'complete') return '✅';
    if (status === 'in_progress') return '🔄';
    if (status === 'active') return '🟢';
    if (status === 'awaiting_approval') return '⏸️';
    return '⏳';
  };

  const statusBadgeClass = (status) => {
    if (status === 'awaiting_approval') return 'badge-warning';
    if (status === 'drip_active' || status === 'active') return 'badge-active';
    if (status === 'completed') return 'badge-completed';
    if (status === 'paused') return 'badge-paused';
    return 'badge-active';
  };

  const statusLabel = (status) => {
    if (status === 'awaiting_approval') return '⏸️ AWAITING APPROVAL';
    if (status === 'drip_active') return 'DRIP_ACTIVE';
    return status?.toUpperCase() || 'UNKNOWN';
  };

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

      {/* ── LEAD REVIEW MODAL ── */}
      {reviewingTask && (
        <div style={{
          position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
          background: 'rgba(0,0,0,0.7)', backdropFilter: 'blur(8px)',
          zIndex: 1000, display: 'flex', alignItems: 'center', justifyContent: 'center',
          padding: 20, animation: 'fadeIn 0.2s'
        }} onClick={() => setReviewingTask(null)}>
          <div style={{
            background: 'var(--bg-primary)', borderRadius: 16,
            border: '1px solid var(--border-subtle)',
            width: '90%', maxWidth: 900, maxHeight: '85vh',
            overflow: 'hidden', display: 'flex', flexDirection: 'column',
            boxShadow: '0 25px 50px -12px rgba(0,0,0,0.6)'
          }} onClick={e => e.stopPropagation()}>
            
            {/* Modal Header */}
            <div style={{
              padding: '20px 24px', borderBottom: '1px solid var(--border-subtle)',
              display: 'flex', justifyContent: 'space-between', alignItems: 'center',
              background: 'var(--bg-secondary)'
            }}>
              <div>
                <h2 style={{ fontSize: '1.2rem', fontWeight: 700, margin: 0 }}>🔍 Review Scraped Leads</h2>
                <div style={{ fontSize: '0.78rem', color: 'var(--text-tertiary)', marginTop: 4 }}>
                  Task: {reviewingTask} • {leadStats.total || 0} leads found • <span style={{ color: '#10b981' }}>{leadStats.with_email || 0} with email</span> • <span style={{ color: '#ef4444' }}>{leadStats.without_email || 0} without</span>
                </div>
              </div>
              <button onClick={() => setReviewingTask(null)} style={{
                background: 'none', border: 'none', color: 'var(--text-secondary)',
                cursor: 'pointer', fontSize: '1.2rem', padding: '4px 8px'
              }}>✕</button>
            </div>

            {/* Modal Body — Lead Table */}
            <div style={{ flex: 1, overflow: 'auto', padding: '16px 24px' }}>
              {loadingLeads ? (
                <div style={{ textAlign: 'center', padding: 40, color: 'var(--text-tertiary)' }}>
                  <div style={{ fontSize: '2rem', marginBottom: 8 }}>⏳</div>
                  Loading leads...
                </div>
              ) : taskLeads.length === 0 ? (
                <div style={{ textAlign: 'center', padding: 40, color: 'var(--text-tertiary)' }}>
                  <div style={{ fontSize: '2rem', marginBottom: 8 }}>📭</div>
                  No leads found for this task
                </div>
              ) : (
                <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.78rem' }}>
                  <thead>
                    <tr style={{ borderBottom: '2px solid var(--border-subtle)', textAlign: 'left' }}>
                      <th style={{ padding: '8px 6px', color: 'var(--text-tertiary)', fontWeight: 600 }}>#</th>
                      <th style={{ padding: '8px 6px', color: 'var(--text-tertiary)', fontWeight: 600 }}>Business</th>
                      <th style={{ padding: '8px 6px', color: 'var(--text-tertiary)', fontWeight: 600 }}>Email</th>
                      <th style={{ padding: '8px 6px', color: 'var(--text-tertiary)', fontWeight: 600 }}>Phone</th>
                      <th style={{ padding: '8px 6px', color: 'var(--text-tertiary)', fontWeight: 600 }}>Rating</th>
                      <th style={{ padding: '8px 6px', color: 'var(--text-tertiary)', fontWeight: 600 }}>Score</th>
                      <th style={{ padding: '8px 6px', color: 'var(--text-tertiary)', fontWeight: 600 }}>Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {taskLeads.map((lead, idx) => (
                      <tr key={lead.id} style={{ borderBottom: '1px solid var(--border-subtle)', transition: 'background 0.15s' }}
                        onMouseEnter={e => e.currentTarget.style.background = 'var(--bg-secondary)'}
                        onMouseLeave={e => e.currentTarget.style.background = 'transparent'}>
                        <td style={{ padding: '10px 6px', color: 'var(--text-tertiary)' }}>{idx + 1}</td>
                        <td style={{ padding: '10px 6px' }}>
                          <div style={{ fontWeight: 600 }}>{lead.business_name || 'Unknown'}</div>
                          <div style={{ fontSize: '0.7rem', color: 'var(--text-tertiary)', marginTop: 2 }}>
                            {lead.full_address || `${lead.city || ''}, ${lead.state || ''}`}
                          </div>
                        </td>
                        <td style={{ padding: '10px 6px' }}>
                          {lead.email_primary ? (
                            <span style={{ color: '#10b981', fontFamily: 'var(--font-mono)', fontSize: '0.72rem' }}>
                              {lead.email_primary}
                            </span>
                          ) : (
                            <span style={{ color: '#ef4444', fontSize: '0.72rem' }}>—</span>
                          )}
                        </td>
                        <td style={{ padding: '10px 6px', fontFamily: 'var(--font-mono)', fontSize: '0.72rem', color: 'var(--text-secondary)' }}>
                          {lead.phone || '—'}
                        </td>
                        <td style={{ padding: '10px 6px' }}>
                          {lead.current_rating > 0 ? (
                            <span>⭐ {Number(lead.current_rating).toFixed(1)} <span style={{ color: 'var(--text-tertiary)', fontSize: '0.68rem' }}>({lead.review_count})</span></span>
                          ) : '—'}
                        </td>
                        <td style={{ padding: '10px 6px' }}>
                          <span style={{
                            display: 'inline-block', padding: '2px 8px', borderRadius: 10,
                            fontSize: '0.7rem', fontWeight: 600,
                            background: lead.lead_score >= 70 ? 'rgba(239,68,68,0.15)' : lead.lead_score >= 40 ? 'rgba(245,158,11,0.15)' : 'rgba(59,130,246,0.15)',
                            color: lead.lead_score >= 70 ? '#ef4444' : lead.lead_score >= 40 ? '#f59e0b' : '#3b82f6'
                          }}>
                            {lead.lead_score || 0}
                          </span>
                        </td>
                        <td style={{ padding: '10px 6px' }}>
                          <span style={{
                            display: 'inline-block', padding: '2px 8px', borderRadius: 10,
                            fontSize: '0.68rem', fontWeight: 500,
                            background: lead.notes === 'verified' ? 'rgba(16,185,129,0.15)' : 'rgba(107,114,128,0.15)',
                            color: lead.notes === 'verified' ? '#10b981' : '#9ca3af'
                          }}>
                            {lead.notes || 'new'}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>

            {/* Modal Footer — Approve Button */}
            <div style={{
              padding: '16px 24px', borderTop: '1px solid var(--border-subtle)',
              display: 'flex', justifyContent: 'space-between', alignItems: 'center',
              background: 'var(--bg-secondary)'
            }}>
              {approveResult && (
                <div style={{
                  fontSize: '0.8rem', flex: 1, marginRight: 16,
                  color: approveResult.includes('❌') ? '#ef4444' : '#10b981'
                }}>
                  {approveResult}
                </div>
              )}
              <div style={{ display: 'flex', gap: 10, marginLeft: 'auto' }}>
                <button className="btn btn-secondary" onClick={() => setReviewingTask(null)}
                  style={{ padding: '10px 20px', fontSize: '0.82rem' }}>
                  Cancel
                </button>
                <button 
                  className="btn btn-primary" 
                  onClick={() => approveTask(reviewingTask)}
                  disabled={approving || (leadStats.with_email || 0) === 0}
                  style={{ 
                    padding: '10px 24px', fontSize: '0.82rem', fontWeight: 700,
                    background: 'linear-gradient(135deg, #10b981, #059669)',
                    display: 'flex', alignItems: 'center', gap: 6
                  }}
                >
                  {approving ? '⏳ Approving...' : `✅ Approve & Start Outreach (${leadStats.with_email || 0} leads)`}
                </button>
              </div>
            </div>
          </div>
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
              <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
                <span className={`badge ${statusBadgeClass(task.status)}`}>{statusLabel(task.status)}</span>
                
                {/* Show Review + Approve buttons when awaiting_approval */}
                {task.status === 'awaiting_approval' && (
                  <>
                    <button className="btn btn-secondary" style={{ padding: '6px 14px', fontSize: '0.74rem', fontWeight: 600 }}
                      onClick={() => reviewLeads(task.id)}>
                      🔍 Review Leads
                    </button>
                    <button className="btn btn-primary" style={{ 
                      padding: '6px 14px', fontSize: '0.74rem', fontWeight: 700,
                      background: 'linear-gradient(135deg, #10b981, #059669)'
                    }}
                      onClick={() => approveTask(task.id)}>
                      ✅ Approve
                    </button>
                  </>
                )}
                
                {task.status === 'active' && <button className="btn btn-secondary" style={{ padding: '4px 12px', fontSize: '0.72rem' }} onClick={() => handleAction(task.id, 'pause')}>⏸ Pause</button>}
                {task.status === 'paused' && <button className="btn btn-success" style={{ padding: '4px 12px', fontSize: '0.72rem' }} onClick={() => handleAction(task.id, 'resume')}>▶ Resume</button>}
              </div>
            </div>

            {/* Awaiting approval banner */}
            {task.status === 'awaiting_approval' && (
              <div style={{
                padding: '10px 16px', borderRadius: 8, marginBottom: 12,
                background: 'rgba(245, 158, 11, 0.12)', border: '1px solid rgba(245, 158, 11, 0.3)',
                fontSize: '0.8rem', color: '#f59e0b', display: 'flex', alignItems: 'center', gap: 8
              }}>
                <span style={{ fontSize: '1.1rem' }}>⚠️</span>
                <span><strong>Scraping complete!</strong> {task.leads_total || 0} leads found. Click "Review Leads" to inspect them, then "Approve" to start outreach.</span>
              </div>
            )}

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
