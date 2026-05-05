import { useState, useEffect } from 'react';
import API from '../config/api.js';

export default function HotLeads() {
  const [leads, setLeads] = useState([]);
  useEffect(() => { fetch(`${API}/api/hot-leads`).then(r => r.json()).then(setLeads).catch(console.error); }, []);

  return (
    <div className="main-content animate-in">
      <div className="page-header">
        <h1>🔥 Hot Leads</h1>
        <p>Leads ready to convert — these are your potential paying clients</p>
      </div>

      {leads.length === 0 ? (
        <div className="glass-card no-hover">
          <div className="empty-state">
            <div className="empty-icon">🔥</div>
            <h3>No hot leads yet</h3>
            <p style={{ color: 'var(--text-tertiary)' }}>Hot leads appear here when prospects show strong engagement or reply with interest. Keep your campaigns running!</p>
          </div>
        </div>
      ) : (
        leads.map(lead => (
          <div className="glass-card" key={lead.id} style={{ marginBottom: 16, borderColor: 'rgba(255,107,107,0.3)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
              <div>
                <h3 style={{ fontSize: '1.1rem', fontWeight: 700 }}>
                  🔥 {lead.business_name}
                </h3>
                <div style={{ fontSize: '0.78rem', color: 'var(--text-secondary)' }}>
                  {lead.owner_name && `${lead.owner_name} • `}{lead.email_primary} • {lead.city} • {lead.niche}
                </div>
              </div>
              <div style={{ display: 'flex', gap: 8 }}>
                <span className="badge badge-hot">HOT LEAD</span>
                <button className="btn btn-success" style={{ padding: '6px 14px', fontSize: '0.78rem' }}>✅ Client Won</button>
              </div>
            </div>

            <div style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', marginBottom: 12 }}>
              ⭐ Rating: {lead.current_rating} • Currently in your Gmail Important folder
            </div>

            <h4 style={{ fontSize: '0.85rem', fontWeight: 600, marginBottom: 8 }}>💬 Conversation History</h4>
            {(lead.conversations || []).length === 0 ? (
              <div style={{ color: 'var(--text-tertiary)', fontSize: '0.78rem' }}>No conversation yet</div>
            ) : (
              lead.conversations.map((conv, i) => (
                <div key={i} style={{ padding: '10px', background: 'var(--bg-input)', borderRadius: 'var(--radius-sm)', marginBottom: 8 }}>
                  <div style={{ fontWeight: 600, fontSize: '0.82rem', marginBottom: 4 }}>RE: {conv.subject}</div>
                  <div style={{ fontSize: '0.78rem', color: 'var(--text-secondary)' }}>{conv.reply}</div>
                  <div style={{ fontSize: '0.65rem', color: 'var(--text-tertiary)', marginTop: 4, fontFamily: 'var(--font-mono)' }}>
                    {conv.replied_at ? new Date(conv.replied_at).toLocaleString() : ''}
                  </div>
                </div>
              ))
            )}
          </div>
        ))
      )}
    </div>
  );
}
