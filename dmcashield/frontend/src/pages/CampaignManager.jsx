import { useState, useEffect } from 'react';
const API = 'http://localhost:8000';

export default function CampaignManager() {
  const [campaigns, setCampaigns] = useState([]);
  const [templates, setTemplates] = useState([]);
  const [showNew, setShowNew] = useState(false);
  const [editing, setEditing] = useState(null);

  const [form, setForm] = useState({
    name: '', subject: '', body: '', variant: 'A', ab_test: false
  });

  useEffect(() => {
    fetchCampaigns();
    fetchTemplates();
  }, []);

  const fetchCampaigns = async () => {
    try {
      const res = await fetch(`${API}/api/campaigns`);
      setCampaigns(await res.json());
    } catch {}
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
        <button className="btn btn-primary" onClick={() => { setShowNew(!showNew); setEditing(null); setForm({ name: '', subject: '', body: '', variant: 'A', ab_test: false }); }}>
          {showNew ? '✕ Cancel' : '+ New Template'}
        </button>
      </div>

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

      {/* Templates */}
      <div className="glass-card no-hover">
        <h3 style={{ marginBottom: 16 }}>📂 Email Templates</h3>
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

        {/* Stats */}
        <div style={{ marginTop: 20, paddingTop: 20, borderTop: '1px solid var(--border-subtle)' }}>
          <div style={{ display: 'flex', gap: 24, fontSize: '0.86rem', color: 'var(--text-secondary)' }}>
            <span><strong style={{ color: 'var(--text-primary)' }}>{templates.length}</strong> Templates</span>
            <span><strong style={{ color: 'var(--text-primary)' }}>{templates.filter(t => t.ab_test).length}</strong> A/B Tests</span>
            <span><strong style={{ color: 'var(--text-primary)' }}>{campaigns.length}</strong> Active Campaigns</span>
          </div>
        </div>
      </div>
    </div>
  );
}