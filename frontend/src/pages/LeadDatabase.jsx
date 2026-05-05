import { useState, useEffect } from 'react';
import API from '../config/api.js';

export default function LeadDatabase() {
  const [leads, setLeads] = useState([]);
  const [filter, setFilter] = useState('all');
  const [selectedLead, setSelectedLead] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => { fetchLeads(); }, [filter]);

  const fetchLeads = async () => {
    try {
      const params = filter !== 'all' ? `?temperature=${filter}` : '';
      const res = await fetch(`${API}/api/leads${params}`);
      setLeads(await res.json());
    } catch (err) { console.error(err); }
    setLoading(false);
  };

  const fetchLeadDetail = async (id) => {
    try {
      const res = await fetch(`${API}/api/leads/${id}`);
      setSelectedLead(await res.json());
    } catch (err) { console.error(err); }
  };

  const filters = ['all', 'cold', 'warm', 'hot', 'converted', 'archived'];

  return (
    <div className="main-content animate-in">
      <div className="page-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <div>
          <h1>👥 Lead Database</h1>
          <p>All scraped and enriched business leads across all campaigns</p>
        </div>
        <button className="btn btn-primary" style={{ padding: '8px 18px', fontSize: '0.82rem' }}
          onClick={() => {
            const params = filter !== 'all' ? `?temperature=${filter}` : '';
            window.open(`${API}/api/leads/export${params}`, '_blank');
          }}>
          📥 Export CSV
        </button>
      </div>

      <div style={{ display: 'flex', gap: 8, marginBottom: 20 }}>
        {filters.map(f => (
          <button key={f} className={`btn ${filter === f ? 'btn-primary' : 'btn-secondary'}`}
            style={{ padding: '6px 14px', fontSize: '0.78rem' }}
            onClick={() => setFilter(f)}>
            {f === 'all' ? '📋 All' : f === 'cold' ? '❄️ Cold' : f === 'warm' ? '🌤️ Warm' : f === 'hot' ? '🔥 Hot' : f === 'converted' ? '✅ Converted' : '📦 Archived'}
          </button>
        ))}
      </div>

      <div style={{ display: 'flex', gap: 20 }}>
        <div className="glass-card no-hover" style={{ flex: 2, overflow: 'auto' }}>
          {leads.length === 0 ? (
            <div className="empty-state">
              <div className="empty-icon">👥</div>
              <h3>No leads yet</h3>
              <p style={{ color: 'var(--text-tertiary)' }}>Launch a task to start scraping leads</p>
            </div>
          ) : (
            <table className="data-table">
              <thead><tr>
                <th>Business</th><th>City</th><th>Rating</th><th>Neg Reviews</th><th>Score</th><th>Status</th><th>Emails</th>
              </tr></thead>
              <tbody>
                {leads.map(lead => (
                  <tr key={lead.id} onClick={() => fetchLeadDetail(lead.id)} style={{ cursor: 'pointer' }}>
                    <td><strong>{lead.business_name}</strong><br/><span style={{ fontSize: '0.72rem', color: 'var(--text-tertiary)' }}>{lead.email_primary}</span></td>
                    <td>{lead.city}, {lead.state}</td>
                    <td>⭐ {lead.current_rating}</td>
                    <td style={{ color: 'var(--accent-hot)' }}>{lead.negative_review_count}</td>
                    <td>{lead.lead_score}/10</td>
                    <td><span className={`badge badge-${lead.lead_temperature}`}>{lead.lead_temperature}</span></td>
                    <td>{lead.emails_sent_count}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>

        {selectedLead && (
          <div className="glass-card no-hover animate-slide" style={{ flex: 1 }}>
            <h3 style={{ fontSize: '1rem', fontWeight: 700, marginBottom: 12 }}>{selectedLead.business_name}</h3>
            <div style={{ fontSize: '0.82rem', display: 'flex', flexDirection: 'column', gap: 8 }}>
              <div><span style={{ color: 'var(--text-tertiary)' }}>Owner:</span> {selectedLead.owner_name || 'Unknown'}</div>
              <div><span style={{ color: 'var(--text-tertiary)' }}>Email:</span> {selectedLead.email_primary}</div>
              <div><span style={{ color: 'var(--text-tertiary)' }}>Phone:</span> {selectedLead.phone || 'N/A'}</div>
              <div><span style={{ color: 'var(--text-tertiary)' }}>Rating:</span> ⭐ {selectedLead.current_rating} ({selectedLead.negative_review_count} negative)</div>
              <div><span style={{ color: 'var(--text-tertiary)' }}>Score:</span> {selectedLead.lead_score}/10</div>
              <div><span style={{ color: 'var(--text-tertiary)' }}>Status:</span> <span className={`badge badge-${selectedLead.lead_temperature}`}>{selectedLead.lead_temperature}</span></div>
              <div><span style={{ color: 'var(--text-tertiary)' }}>Funnel Step:</span> {selectedLead.funnel_step}/6</div>
            </div>
            <h4 style={{ marginTop: 16, fontSize: '0.88rem', fontWeight: 600 }}>📧 Email History</h4>
            {(selectedLead.email_history || []).length === 0 ? (
              <div style={{ color: 'var(--text-tertiary)', fontSize: '0.78rem', marginTop: 8 }}>No emails sent yet</div>
            ) : (
              selectedLead.email_history.map((e, i) => (
                <div key={i} style={{ padding: '8px 0', borderBottom: '1px solid var(--border-subtle)', fontSize: '0.78rem' }}>
                  <div style={{ fontWeight: 600 }}>Email #{e.email_number}: {e.subject_line}</div>
                  <div style={{ color: 'var(--text-tertiary)' }}>
                    {e.opened ? `✅ Opened (${e.open_count}x)` : '❌ Not opened'} {e.replied ? '💬 Replied' : ''}
                  </div>
                </div>
              ))
            )}
            <button className="btn btn-secondary" style={{ marginTop: 16, width: '100%', justifyContent: 'center' }} onClick={() => setSelectedLead(null)}>Close</button>
          </div>
        )}
      </div>
    </div>
  );
}
