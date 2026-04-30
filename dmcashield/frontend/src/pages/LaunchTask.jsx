import { useState } from 'react';

const API = 'http://localhost:8000';

export default function LaunchTask() {
  const [form, setForm] = useState({ business_type: '', city: '', state: '', country: 'USA' });
  const [launching, setLaunching] = useState(false);
  const [result, setResult] = useState(null);
  const [tasks, setTasks] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!form.business_type || !form.city || !form.state) return;
    setLaunching(true);
    try {
      const res = await fetch(`${API}/api/tasks`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      });
      const data = await res.json();
      setResult(data);
      setTasks(prev => [data.task, ...prev]);
      setForm({ business_type: '', city: '', state: '', country: 'USA' });
    } catch (err) {
      setResult({ error: 'Failed to connect to backend' });
    }
    setLaunching(false);
  };

  const BUSINESS_TYPES = ['Dentist', 'Restaurant', 'Salon', 'Hotel', 'Law Firm', 'Gym', 'Clinic', 'Chiropractor', 'Plumber', 'Electrician', 'Auto Repair', 'Real Estate', 'Veterinarian', 'Spa', 'Barbershop'];

  return (
    <div className="main-content animate-in">
      <div className="page-header">
        <h1>🚀 Launch New Task</h1>
        <p>Enter a business type and location to start scraping leads and launching outreach</p>
      </div>

      <div className="grid-2">
        <div className="glass-card no-hover">
          <h3 style={{ marginBottom: 20, fontSize: '1rem', fontWeight: 700 }}>📋 New Campaign</h3>
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label className="form-label">Business Type</label>
              <select className="form-select" value={form.business_type} onChange={e => setForm({...form, business_type: e.target.value})}>
                <option value="">Select business type...</option>
                {BUSINESS_TYPES.map(t => <option key={t} value={t.toLowerCase()}>{t}</option>)}
              </select>
            </div>
            <div className="form-group">
              <label className="form-label">City</label>
              <input className="form-input" placeholder="e.g. Houston" value={form.city} onChange={e => setForm({...form, city: e.target.value})} />
            </div>
            <div className="form-group">
              <label className="form-label">State / Province</label>
              <input className="form-input" placeholder="e.g. Texas" value={form.state} onChange={e => setForm({...form, state: e.target.value})} />
            </div>
            <div className="form-group">
              <label className="form-label">Country</label>
              <input className="form-input" placeholder="USA" value={form.country} onChange={e => setForm({...form, country: e.target.value})} />
            </div>
            <button className="btn btn-primary" type="submit" disabled={launching} style={{ width: '100%', justifyContent: 'center', marginTop: 8 }}>
              {launching ? '⏳ Launching...' : '🚀 Launch Campaign'}
            </button>
          </form>

          {result && (
            <div style={{ marginTop: 20, padding: 16, background: result.error ? 'rgba(255,107,107,0.1)' : 'rgba(0,184,148,0.1)', borderRadius: 'var(--radius-sm)', border: `1px solid ${result.error ? 'rgba(255,107,107,0.3)' : 'rgba(0,184,148,0.3)'}` }}>
              <div style={{ fontSize: '0.82rem', color: result.error ? 'var(--accent-hot)' : 'var(--accent-success)' }}>
                {result.error ? `❌ ${result.error}` : `✅ Task launched! ID: ${result.task_id || result.task?.id}`}
              </div>
            </div>
          )}
        </div>

        <div className="glass-card no-hover">
          <h3 style={{ marginBottom: 16, fontSize: '1rem', fontWeight: 700 }}>💡 How It Works</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
            {[
              { step: 1, icon: '🔍', title: 'Scraping', desc: 'DataHunter agents scrape Google Maps for businesses matching your criteria' },
              { step: 2, icon: '✅', title: 'Validation', desc: 'Emails verified, data enriched, competitors analyzed' },
              { step: 3, icon: '📝', title: 'Copywriting', desc: 'AI writes personalized emails using emotional triggers & competitor data' },
              { step: 4, icon: '📤', title: 'Sending', desc: 'Emails sent with smart throttling, warmup, and multi-account rotation' },
              { step: 5, icon: '📊', title: 'Tracking', desc: 'Every open, click, and reply tracked and analyzed' },
              { step: 6, icon: '💼', title: 'Sales', desc: 'AI handles replies like a human. Hot leads marked as Important in Gmail' },
            ].map(s => (
              <div key={s.step} style={{ display: 'flex', gap: 14, alignItems: 'flex-start' }}>
                <div style={{ width: 36, height: 36, borderRadius: '50%', background: 'rgba(108,92,231,0.12)', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0, fontSize: '1rem' }}>{s.icon}</div>
                <div>
                  <div style={{ fontWeight: 600, fontSize: '0.88rem' }}>Step {s.step}: {s.title}</div>
                  <div style={{ fontSize: '0.78rem', color: 'var(--text-secondary)' }}>{s.desc}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
