import React, { useState, useEffect } from 'react';

export default function HotLeads() {
  const [leads, setLeads] = useState([]);

  useEffect(() => {
    fetch('/api/leads?temperature=hot')
      .then(r => r.json())
      .then(setLeads);
  }, []);

  return (
    <div className="hot-leads">
      <h1>🔥 Hot Leads Ready to Convert</h1>
      <p className="subtitle">These leads require your attention in Gmail "Important" folder</p>
      <div className="lead-list">
        {leads.map(lead => (
          <div key={lead.id} className="lead-card">
            <h3>{lead.business_name}</h3>
            <p><strong>Owner:</strong> {lead.owner_name}</p>
            <p><strong>Email:</strong> {lead.email_primary}</p>
            <p><strong>Location:</strong> {lead.city}, {lead.state}</p>
            <p><strong>Rating:</strong> {lead.current_rating}★ ({lead.negative_review_count} negative)</p>
            <div className="competitor-info">
              <strong>Competitors:</strong>
              {lead.competitor_info?.competitors?.map(c =>
                <span key={c.name}>{c.name} ({c.rating}★) </span>
              )}
            </div>
            <button className="contact-btn">Contact</button>
          </div>
        ))}
      </div>
    </div>
  );
}