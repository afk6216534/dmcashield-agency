import { useState, useEffect } from 'react';
import API from '../config/api.js';

export default function CampaignManager() {
  const [campaigns, setCampaigns] = useState([]);
  const [templates, setTemplates] = useState([]);
  const [showNew, setShowNew] = useState(false);
  const [editing, setEditing] = useState(null);

  const [form, setForm] = useState({
    name: '', subject: '', body: '', variant: 'A', ab_test: false
  });

  // V5.0 Real Campaigns State
  const [realCampaigns, setRealCampaigns] = useState([]);
  const [showNewCampaign, setShowNewCampaign] = useState(false);
  const [campaignForm, setCampaignForm] = useState({ name: '', niche: '', city: '', state: '' });
  const [sendingBatchId, setSendingBatchId] = useState(null);
  const [batchSize, setBatchSize] = useState(10);
  const [batchResult, setBatchResult] = useState(null);

  useEffect(() => {
    fetchCampaigns();
    fetchTemplates();
    fetchRealCampaigns();
  }, []);

  const fetchCampaigns = async () => {
    try {
      const res = await fetch(`${API}/api/campaigns`);
      setCampaigns(await res.json());
    } catch {}
  };

  const fetchRealCampaigns = async () => {
    try {
      const res = await fetch(`${API}/api/campaigns/real`);
      const data = await res.json();
      setRealCampaigns(data.campaigns || []);
    } catch (err) {
      console.error(err);
    }
  };

  const fetchTemplates = async () => {
    try {
      const res = await fetch(`${API}/api/templates`);
      setTemplates(await res.json());
    } catch {}
  };

  const handleSave = async (e) => {
    e.preventDefault();
    try {
      const method = editing ? 'PUT' : 'POST';
      const url = editing ? `${API}/api/templates/${editing.id}` : `${API}/api/templates`;
      await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form)
      });
      setForm({ name: '', subject: '', body: '', variant: 'A', ab_test: false });
      setShowNew(false);
      setEditing(null);
      fetchTemplates();
    } catch {}
  };

  const handleDelete = async (id) => {
    if (!confirm('Delete this template?')) return;
    await fetch(`${API}/api/templates/${id}`, { method: 'DELETE' });
    fetchTemplates();
  };

  const handleCreateCampaign = async (e) => {
    e.preventDefault();
    if (!campaignForm.name || !campaignForm.niche) return;
    try {
      const res = await fetch(`${API}/api/campaigns/create`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(campaignForm)
      });
      if (res.ok) {
        setCampaignForm({ name: '', niche: '', city: '', state: '' });
        setShowNewCampaign(false);
        fetchRealCampaigns();
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleRunBatch = async (id) => {
    setSendingBatchId(id);
    setBatchResult(null);
    try {
      const res = await fetch(`${API}/api/campaigns/${id}/send`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ batch_size: batchSize })
      });
      const data = await res.json();
      setBatchResult({ id, ...data });
      fetchRealCampaigns();
    } catch (err) {
      console.error(err);
    }
    setSendingBatchId(null);
  };

  const duplicateTemplate = (t) => {
    setForm({ ...t, name: `${t.name} (Copy)`, id: undefined });
    setEditing(null);
    setShowNew(true);
  };

  return (
    <div className="main-content animate-in">
      <div className="page-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <div>
          <h1>📧 Campaign Manager</h1>
          <p>Email templates, A/B testing, and campaign management</p>
        </div>
        <div style={{ display: 'flex', gap: 8 }}>
          <button className="btn btn-secondary" onClick={() => setShowNewCampaign(!showNewCampaign)}>
            {showNewCampaign ? '✕ Cancel Campaign' : '🚀 New Campaign'}
          </button>
          <button className="btn btn-primary" onClick={() => { setShowNew(!showNew); setEditing(null); setForm({ name: '', subject: '', body: '', variant: 'A', ab_test: false }); }}>
            {showNew ? '✕ Cancel Template' : '+ New Template'}
          </button>
        </div>
      </div>

      {showNewCampaign && (
        <div className="glass-card no-hover animate-in" style={{ marginBottom: 20 }}>
          <h3 style={{ marginBottom: 16 }}>🚀 Create Real Outreach Campaign</h3>
          <form onSubmit={handleCreateCampaign} style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr 1fr auto', gap: 12, alignItems: 'end' }}>
            <div className="form-group" style={{ margin: 0 }}>
              <label className="form-label">Campaign Name</label>
              <input className="form-input" placeholder="e.g. Chicago Dentists" value={campaignForm.name} onChange={e => setCampaignForm({...campaignForm, name: e.target.value})} required />
            </div>
            <div className="form-group" style={{ margin: 0 }}>
              <label className="form-label">Niche</label>
              <input className="form-input" placeholder="e.g. dentist" value={campaignForm.niche} onChange={e => setCampaignForm({...campaignForm, niche: e.target.value})} required />
            </div>
            <div className="form-group" style={{ margin: 0 }}>
              <label className="form-label">City</label>
              <input className="form-input" placeholder="e.g. Chicago" value={campaignForm.city} onChange={e => setCampaignForm({...campaignForm, city: e.target.value})} />
            </div>
            <div className="form-group" style={{ margin: 0 }}>
              <label className="form-label">State</label>
              <input className="form-input" placeholder="e.g. Illinois" value={campaignForm.state} onChange={e => setCampaignForm({...campaignForm, state: e.target.value})} />
            </div>
            <button className="btn btn-success" type="submit">Create Campaign</button>
          </form>
        </div>
      )}

      {showNew && (
        <div className="glass-card no-hover animate-in" style={{ marginBottom: 20 }}>
          <h3 style={{ marginBottom: 16 }}>{editing ? '✏ Edit Template' : '📝 New Email Template'}</h3>
          
          <div style={{ display: 'flex', gap: 12, marginBottom: 16 }}>
            <label style={{ display: 'flex', alignItems: 'center', gap: 8, cursor: 'pointer' }}>
              <input type="checkbox" checked={form.ab_test} onChange={e => setForm({ ...form, ab_test: e.target.checked })} />
              <span style={{ fontSize: '0.86rem' }}>Enable A/B Testing</span>
            </label>
          </div>

          <div className="form-group">
            <label className="form-label">Template Name</label>
            <input className="form-input" placeholder="e.g., Welcome Sequence" value={form.name} onChange={e => setForm({ ...form, name: e.target.value })} />
          </div>

          <div className="form-group">
            <label className="form-label">Subject Line</label>
            <input className="form-input" placeholder="e.g., {{name}}, need help with your reviews?" value={form.subject} onChange={e => setForm({ ...form, subject: e.target.value })} />
            <p style={{ fontSize: '0.72rem', color: 'var(--text-tertiary)', marginTop: 4 }}>Use {"{{name}}"} for personalization</p>
          </div>

          {form.ab_test && (
            <div className="grid-2" style={{ marginBottom: 16 }}>
              <div className="form-group">
                <label className="form-label">Variant A Subject</label>
                <input className="form-input" placeholder="Variant A subject" value={form.variant_a || ''} onChange={e => setForm({ ...form, variant_a: e.target.value })} />
              </div>
              <div className="form-group">
                <label className="form-label">Variant B Subject</label>
                <input className="form-input" placeholder="Variant B subject" value={form.variant_b || ''} onChange={e => setForm({ ...form, variant_b: e.target.value })} />
              </div>
            </div>
          )}

          <div className="form-group">
            <label className="form-label">Email Body</label>
            <textarea className="form-input" rows={8} placeholder="Hi {{name}},&#10;&#10;I help businesses like yours..." value={form.body} onChange={e => setForm({ ...form, body: e.target.value })} />
          </div>

          <button className="btn btn-success" onClick={handleSave}>{editing ? '💾 Save Changes' : '✅ Create Template'}</button>
        </div>
      )}

      {/* Two Column Layout for Templates and Campaigns */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20 }}>
        {/* Left Column: Email Templates */}
        <div className="glass-card no-hover" style={{ height: 'fit-content' }}>
          <h3 style={{ marginBottom: 16, borderBottom: '1px solid var(--border-subtle)', paddingBottom: 10 }}>📂 Email Templates</h3>
          {templates.length === 0 ? (
            <div className="empty-state">
              <div className="empty-icon">📧</div>
              <h3>No templates yet</h3>
              <p style={{ color: 'var(--text-tertiary)' }}>Create your first email template</p>
            </div>
          ) : (
            <div style={{ display: 'grid', gap: 12 }}>
              {templates.map((t, i) => (
                <div key={i} className="template-card" style={{ padding: 16, background: 'var(--bg-tertiary)', borderRadius: 12 }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                    <div>
                      <div style={{ fontWeight: 600, marginBottom: 4 }}>{t.name}</div>
                      <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: 8 }}>Subject: {t.subject}</div>
                      {t.ab_test && <span className="badge badge-warm" style={{ fontSize: '0.68rem' }}>A/B Test</span>}
                    </div>
                    <div style={{ display: 'flex', gap: 8 }}>
                      <button className="btn" style={{ padding: '6px 12px', fontSize: '0.76rem' }} onClick={() => { setEditing(t); setForm(t); setShowNew(true); }}>Edit</button>
                      <button className="btn" style={{ padding: '6px 12px', fontSize: '0.76rem' }} onClick={() => duplicateTemplate(t)}>Copy</button>
                      <button className="btn btn-danger" style={{ padding: '6px 12px', fontSize: '0.76rem' }} onClick={() => handleDelete(t.id)}>Delete</button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
          <div style={{ marginTop: 20, paddingTop: 20, borderTop: '1px solid var(--border-subtle)' }}>
            <div style={{ display: 'flex', gap: 24, fontSize: '0.86rem', color: 'var(--text-secondary)' }}>
              <span><strong style={{ color: 'var(--text-primary)' }}>{templates.length}</strong> Templates</span>
              <span><strong style={{ color: 'var(--text-primary)' }}>{templates.filter(t => t.ab_test).length}</strong> A/B Tests</span>
            </div>
          </div>
        </div>

        {/* Right Column: Real Campaigns and Batch Trigger */}
        <div className="glass-card no-hover">
          <h3 style={{ marginBottom: 16, borderBottom: '1px solid var(--border-subtle)', paddingBottom: 10 }}>🔒 Active Real Campaigns</h3>
          
          <div style={{ marginBottom: 16, display: 'flex', alignItems: 'center', gap: 8 }}>
            <label style={{ fontSize: '0.82rem', color: 'var(--text-secondary)' }}>Batch Send Size:</label>
            <input className="form-input" type="number" style={{ width: 70, padding: '4px 8px', margin: 0 }} value={batchSize} onChange={e => setBatchSize(parseInt(e.target.value) || 10)} min={1} max={50} />
          </div>

          {realCampaigns.length === 0 ? (
            <div className="empty-state">
              <div className="empty-icon">🚀</div>
              <h3>No real campaigns created</h3>
              <p style={{ color: 'var(--text-tertiary)' }}>Click "New Campaign" at the top to configure your first active run</p>
            </div>
          ) : (
            <div style={{ display: 'grid', gap: 12 }}>
              {realCampaigns.map((camp, i) => (
                <div key={camp.id} style={{ padding: 16, background: 'var(--bg-tertiary)', borderRadius: 12, border: '1px solid var(--border-subtle)' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
                    <div>
                      <div style={{ fontWeight: 600, fontSize: '0.94rem' }}>{camp.name}</div>
                      <div style={{ fontSize: '0.74rem', color: 'var(--text-tertiary)' }}>Target: {camp.niche} in {camp.city || 'Any'}, {camp.state || 'Any'}</div>
                    </div>
                    <button className="btn btn-primary" style={{ padding: '6px 14px', fontSize: '0.78rem' }} onClick={() => handleRunBatch(camp.id)} disabled={sendingBatchId === camp.id}>
                      {sendingBatchId === camp.id ? '⏳ Sending...' : '📤 Run Batch'}
                    </button>
                  </div>

                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 8, background: 'var(--bg-input)', padding: 8, borderRadius: 8, textAlign: 'center', fontSize: '0.74rem' }}>
                    <div>
                      <div style={{ fontWeight: 600, color: 'var(--text-primary)' }}>{camp.total_leads || 0}</div>
                      <div style={{ color: 'var(--text-tertiary)', fontSize: '0.65rem' }}>Leads</div>
                    </div>
                    <div>
                      <div style={{ fontWeight: 600, color: 'var(--text-primary)' }}>{camp.emails_sent || 0}</div>
                      <div style={{ color: 'var(--text-tertiary)', fontSize: '0.65rem' }}>Sent</div>
                    </div>
                    <div>
                      <div style={{ fontWeight: 600, color: 'var(--accent-success)' }}>{camp.opens || 0}</div>
                      <div style={{ color: 'var(--text-tertiary)', fontSize: '0.65rem' }}>Opens</div>
                    </div>
                    <div>
                      <div style={{ fontWeight: 600, color: 'var(--accent-primary)' }}>{camp.replies || 0}</div>
                      <div style={{ color: 'var(--text-tertiary)', fontSize: '0.65rem' }}>Replies</div>
                    </div>
                  </div>

                  {batchResult && batchResult.id === camp.id && (
                    <div style={{ marginTop: 12, padding: 10, background: 'rgba(0,184,148,0.1)', border: '1px solid rgba(0,184,148,0.2)', borderRadius: 6, fontSize: '0.74rem', color: 'var(--accent-success)' }}>
                      <div>Batch send complete: Sent: {batchResult.sent} | Skipped: {batchResult.skipped} | Errors: {batchResult.errors}</div>
                      {batchResult.next_send_in && <div style={{ fontSize: '0.68rem', color: 'var(--text-tertiary)', marginTop: 2 }}>Throttling: next send in {batchResult.next_send_in}</div>}
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}