import React, { useState, useEffect } from 'react';

export default function LeadDatabase() {
  const [leads, setLeads] = useState([]);
  const [filter, setFilter] = useState({ temperature: '', status: '' });

  useEffect(() => {
    fetch('/api/leads?' + new URLSearchParams(filter))
      .then(r => r.json())
      .then(setLeads);
  }, [filter]);

  return (
    <div className="lead-db">
      <h1>Lead Database</h1>
      <div className="filters">
        <select onChange={e => setFilter(f => ({...f, temperature: e.target.value}))}>
          <option value="">All Temperatures</option>
          <option value="cold">Cold</option>
          <option value="warm">Warm</option>
          <option value="hot">Hot</option>
        </select>
      </div>
      <table>
        <thead><tr><th>Business</th><th>Email</th><th>City</th><th>Temp</th><th>Rating</th></tr></thead>
        <tbody>
          {leads.map(lead => (
            <tr key={lead.id} className={lead.temperature}>
              <td>{lead.business_name}</td>
              <td>{lead.email_primary}</td>
              <td>{lead.city}</td>
              <td><span className={`badge ${lead.temperature}`}>{lead.temperature}</span></td>
              <td>{lead.rating}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}