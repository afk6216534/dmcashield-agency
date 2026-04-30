import { useState, useEffect } from 'react';
const API = 'http://localhost:8000';

export default function CampaignScheduler() {
  const [scheduled, setScheduled] = useState([
    { id: 1, name: 'Dental LA Campaign', scheduled_for: '2026-05-01T09:00', status: 'scheduled' },
    { id: 2, name: 'Pizza NYC Campaign', scheduled_for: '2026-05-02T14:00', status: 'scheduled' },
  ]);

  const [form, setForm] = useState({ name: '', date: '', time: '', business_type: '', city: '', state: '' });

  const handleSchedule = async (e) => {
    e.preventDefault();
    setScheduled([...scheduled, { ...form, id: Date.now(), status: 'scheduled' }]);
    setForm({ name: '', date: '', time: '', business_type: '', city: '', state: '' });
  };

  const cancelCampaign = (id) => {
    setScheduled(scheduled.filter(c => c.id !== id));
  };

  return (
    <div className="main-content animate-in">
      <div className="page-header">
        <h1>📅 Campaign Scheduler</h1>
        <p>Schedule and automate your campaigns</p>
      </div>

      {/* Schedule Form */}
      <div className="glass-card no-hover" style={{ marginBottom: 20 }}>
        <h3 style={{ marginBottom: 16 }}>⏰ Schedule New Campaign</h3>
        <form onSubmit={handleSchedule} className="grid-2">
          <div className="form-group">
            <label className="form-label">Campaign Name</label>
            <input className="form-input" value={form.name} onChange={e => setForm({ ...form, name: e.target.value })} />
          </div>
          <div className="form-group">
            <label className="form-label">Business Type</label>
            <select className="form-input" value={form.business_type} onChange={e => setForm({ ...form, business_type: e.target.value })}>
              <option value="">Select type</option>
              <option>Dental Practice</option>
              <option>Pizza Shop</option>
              <option>Law Firm</option>
              <option>Restaurant</option>
            </select>
          </div>
          <div className="form-group">
            <label className="form-label">Date</label>
            <input className="form-input" type="date" value={form.date} onChange={e => setForm({ ...form, date: e.target.value })} />
          </div>
          <div className="form-group">
            <label className="form-label">Time</label>
            <input className="form-input" type="time" value={form.time} onChange={e => setForm({ ...form, time: e.target.value })} />
          </div>
          <div className="form-group">
            <label className="form-label">City</label>
            <input className="form-input" value={form.city} onChange={e => setForm({ ...form, city: e.target.value })} />
          </div>
          <div className="form-group">
            <label className="form-label">State</label>
            <input className="form-input" value={form.state} onChange={e => setForm({ ...form, state: e.target.value })} />
          </div>
        </form>
        <button className="btn btn-primary" type="submit" onClick={handleSchedule}>📅 Schedule Campaign</button>
      </div>

      {/* Scheduled List */}
      <div className="glass-card no-hover">
        <h3 style={{ marginBottom: 16 }}>📋 Scheduled Campaigns</h3>
        {scheduled.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon">📅</div>
            <h3>No scheduled campaigns</h3>
          </div>
        ) : (
          scheduled.map((camp, i) => (
            <div key={i} style={{ padding: 16, background: 'var(--bg-tertiary)', borderRadius: 12, marginBottom: 12 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                  <div style={{ fontWeight: 600 }}>{camp.name}</div>
                  <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                    ⏰ {camp.scheduled_for || `${camp.date} ${camp.time}`}
                  </div>
                </div>
                <div style={{ display: 'flex', gap: 8 }}>
                  <span className="badge badge-warm">Scheduled</span>
                  <button className="btn btn-danger" style={{ padding: '6px 12px', fontSize: '0.72rem' }} onClick={() => cancelCampaign(camp.id)}>Cancel</button>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}