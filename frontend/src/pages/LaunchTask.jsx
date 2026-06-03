import { useState, useEffect } from 'react';
import API from '../config/api.js';

export default function LaunchTask() {
  const [form, setForm] = useState({ business_type: '', city: '', state: '', country: 'USA', max_results: 20 });
  const [launching, setLaunching] = useState(false);
  const [result, setResult] = useState(null);
  const [scrapeTasks, setScrapeTasks] = useState([]);

  useEffect(() => {
    fetchScrapeTasks();
  }, []);

  const fetchScrapeTasks = async () => {
    try {
      const res = await fetch(`${API}/api/scrape/tasks`);
      const data = await res.json();
      setScrapeTasks(data.tasks || []);
    } catch (err) {
      console.error('Failed to load scraping tasks', err);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!form.business_type || !form.city || !form.state) return;
    setLaunching(true);
    setResult(null);
    try {
      const res = await fetch(`${API}/api/scrape`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      });
      const data = await res.json();
      setResult(data);
      if (!data.error) {
        setForm({ business_type: '', city: '', state: '', country: 'USA', max_results: 20 });
      }
      fetchScrapeTasks();
    } catch (err) {
      setResult({ error: 'Failed to connect to backend' });
    }
    setLaunching(false);
  };

  const BUSINESS_TYPES = ['Dentist', 'Restaurant', 'Salon', 'Hotel', 'Law Firm', 'Gym', 'Clinic', 'Chiropractor', 'Plumber', 'Electrician', 'Auto Repair', 'Real Estate', 'Veterinarian', 'Spa', 'Barbershop'];

  return (
    <div className="main-content animate-in">
      <div className="page-header">
        <h1>🚀 Launch New Real Scraper</h1>
        <p>Enter a business type and location to start scraping real leads from web directories</p>
      </div>

      <div className="grid-2">
        <div className="glass-card no-hover">
          <h3 style={{ marginBottom: 20, fontSize: '1rem', fontWeight: 700 }}>📋 New Scraping Task</h3>
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
              <input className="form-input" placeholder="e.g. Houston" value={form.city} onChange={e => setForm({...form, city: e.target.value})} required />
            </div>
            <div className="form-group">
              <label className="form-label">State / Province</label>
              <input className="form-input" placeholder="e.g. Texas" value={form.state} onChange={e => setForm({...form, state: e.target.value})} required />
            </div>
            <div className="form-group">
              <label className="form-label">Country</label>
              <input className="form-input" placeholder="USA" value={form.country} onChange={e => setForm({...form, country: e.target.value})} />
            </div>
            <div className="form-group">
              <label className="form-label">Max Results</label>
              <input className="form-input" type="number" placeholder="20" value={form.max_results} onChange={e => setForm({...form, max_results: parseInt(e.target.value) || 20})} min={1} max={50} />
            </div>
            <button className="btn btn-primary" type="submit" disabled={launching} style={{ width: '100%', justifyContent: 'center', marginTop: 8 }}>
              {launching ? '⏳ Scraping & Enriched Lead Gen Running...' : '🚀 Launch Scraper'}
            </button>
          </form>

          {result && (
            <div style={{ marginTop: 20, padding: 16, background: result.error ? 'rgba(255,107,107,0.1)' : 'rgba(0,184,148,0.1)', borderRadius: 'var(--radius-sm)', border: `1px solid ${result.error ? 'rgba(255,107,107,0.3)' : 'rgba(0,184,148,0.3)'}` }}>
              <div style={{ fontSize: '0.82rem', color: result.error ? 'var(--accent-hot)' : 'var(--accent-success)' }}>
                {result.error ? (
                  <>❌ Error: {result.error}</>
                ) : (
                  <>
                    <div style={{ fontWeight: 700, marginBottom: 4 }}>✅ Scraping Pipeline Complete!</div>
                    <div>Task ID: <code style={{fontFamily: 'monospace'}}>{result.task_id}</code></div>
                    <div>Leads Scraped: {result.leads_scraped}</div>
                    <div>Leads Saved to DB: {result.leads_saved}</div>
                  </>
                )}
              </div>
            </div>
          )}
        </div>

        <div className="glass-card no-hover">
          <h3 style={{ marginBottom: 16, fontSize: '1rem', fontWeight: 700 }}>💡 How It Works</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
            {[
              { step: 1, icon: '🔍', title: 'HTTP Scraping', desc: 'Direct, serverless-safe extraction from YellowPages and Yelp (fast, no heavy browser needed).' },
              { step: 2, icon: '🌐', title: 'Website Extraction', desc: 'Automatically crawls business homepages, /about, /contact for emails and contact details.' },
              { step: 3, icon: '✅', title: 'Data Validation', desc: 'Validates phone formats, normalizes emails, analyzes current ratings.' },
              { step: 4, icon: '📈', title: 'Lead Scoring', desc: 'Calculates closing probability based on low Yelp/YP ratings & bad review volumes.' },
              { step: 5, icon: '💾', title: 'Cloud DB Storage', desc: 'Saves leads immediately to database, ready to be toggle-viewed in Lead Database page.' },
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

      <div className="glass-card no-hover" style={{ marginTop: 20 }}>
        <h3 style={{ marginBottom: 16, fontSize: '1rem', fontWeight: 700 }}>📜 Scraping Task History</h3>
        {scrapeTasks.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon">📜</div>
            <h3>No scraping history</h3>
            <p style={{ color: 'var(--text-tertiary)' }}>Tasks you launch will appear here</p>
          </div>
        ) : (
          <table className="data-table">
            <thead>
              <tr>
                <th>Task ID</th>
                <th>Target</th>
                <th>Status</th>
                <th>Leads Found</th>
                <th>Launched At</th>
              </tr>
            </thead>
            <tbody>
              {scrapeTasks.map(t => (
                <tr key={t.id}>
                  <td><code style={{ fontFamily: 'monospace', fontSize: '0.75rem' }}>{t.id}</code></td>
                  <td><strong>{t.business_type}</strong> in {t.city}, {t.state} ({t.country})</td>
                  <td>
                    <span className={`badge badge-${t.status === 'complete' ? 'success' : t.status === 'scraping' ? 'warm' : 'danger'}`}>
                      {t.status}
                    </span>
                  </td>
                  <td>{t.leads_found || 0}</td>
                  <td style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
                    {t.created_at ? new Date(t.created_at).toLocaleString() : 'N/A'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
