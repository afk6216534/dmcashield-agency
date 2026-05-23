import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function LeadDetails() {
  const { id } = useParams();
  const [lead, setLead] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    fetch(`${API}/api/leads/${id}/full`)
      .then(r => r.json())
      .then(d => { setLead(d); setLoading(false); })
      .catch(() => setLoading(false));
  }, [id]);

  if (loading) return <div className="page-container"><div className="loading">Loading lead details...</div></div>;
  if (!lead) return <div className="page-container"><div className="error">Lead not found</div></div>;

  const tempColor = { hot: '#22c55e', warm: '#f59e0b', cold: '#6b7280' }[lead.lead_temperature] || '#6b7280';

  return (
    <div className="page-container">
      <div className="lead-details-header">
        <div className="header-left">
          <h1>{lead.business_name}</h1>
          <span className={`temperature-badge`} style={{ background: tempColor }}>
            {lead.lead_temperature.toUpperCase()}
          </span>
          {lead.gmail_important && <span className="important-badge">★ Gmail Important</span>}
        </div>
        <div className="header-right">
          <div className="score-display">
            <div className="score-label">Lead Score</div>
            <div className="score-value">{lead.lead_score}</div>
          </div>
          <div className="score-display">
            <div className="score-label">Closing %</div>
            <div className="score-value">{lead.closing_probability}%</div>
          </div>
        </div>
      </div>

      <div className="tabs">
        {['overview', 'business', 'owner', 'analysis', 'interactions', 'call-guide'].map(tab => (
          <button key={tab} className={activeTab === tab ? 'active' : ''} onClick={() => setActiveTab(tab)}>
            {tab.replace('-', ' ').toUpperCase()}
          </button>
        ))}
      </div>

      <div className="tab-content">
        {activeTab === 'overview' && (
          <div className="overview-grid">
            <div className="info-card">
              <h3>Contact Information</h3>
              <div className="info-row"><span>Owner:</span><strong>{lead.owner_name}</strong></div>
              <div className="info-row"><span>Email:</span><a href={`mailto:${lead.email_primary}`}>{lead.email_primary}</a></div>
              <div className="info-row"><span>Phone:</span><a href={`tel:${lead.phone}`}>{lead.phone}</a></div>
              <div className="info-row"><span>Website:</span><a href={lead.website} target="_blank" rel="noreferrer">{lead.website}</a></div>
              <div className="info-row"><span>Address:</span>{lead.full_address}</div>
            </div>
            <div className="info-card">
              <h3>Business Summary</h3>
              <div className="info-row"><span>Niche:</span><strong>{lead.niche}</strong></div>
              <div className="info-row"><span>Nature:</span>{lead.business_nature}</div>
              <div className="info-row"><span>Years:</span>{lead.years_in_business} years</div>
              <div className="info-row"><span>Employees:</span>{lead.employee_count}</div>
              <div className="info-row"><span>Revenue:</span>{lead.revenue_range}</div>
            </div>
            <div className="info-card">
              <h3>Reputation Scores</h3>
              <div className="rating-bars">
                {Object.entries(lead.review_platforms || {}).map(([platform, rating]) => (
                  <div key={platform} className="rating-bar">
                    <span className="platform">{platform}</span>
                    <div className="bar"><div className="fill" style={{ width: `${(rating/5)*100}%` }}></div></div>
                    <span className="value">{rating}</span>
                  </div>
                ))}
              </div>
              <div className="info-row"><span>Negative Reviews:</span><span className="negative">{lead.negative_review_count}</span></div>
            </div>
            {lead.important_notes && (
              <div className="info-card important-notes">
                <h3>★ Important Notes</h3>
                <p>{lead.important_notes}</p>
              </div>
            )}
          </div>
        )}

        {activeTab === 'business' && (
          <div className="business-details">
            <div className="info-card">
              <h3>Business Overview</h3>
              <div className="info-row"><span>Business Name:</span><strong>{lead.business_name}</strong></div>
              <div className="info-row"><span>Nature of Business:</span>{lead.business_nature}</div>
              <div className="info-row"><span>Industry/Niche:</span>{lead.niche}</div>
              <div className="info-row"><span>Years in Business:</span>{lead.years_in_business}</div>
              <div className="info-row"><span>Employee Count:</span>{lead.employee_count}</div>
              <div className="info-row"><span>Revenue Range:</span>{lead.revenue_range}</div>
            </div>
            <div className="info-card">
              <h3>Location</h3>
              <div className="info-row"><span>Address:</span>{lead.full_address}</div>
              <div className="info-row"><span>City:</span>{lead.city}, {lead.state}</div>
              <div className="info-row"><span>Website:</span><a href={lead.website} target="_blank" rel="noreferrer">{lead.website}</a></div>
            </div>
            <div className="info-card">
              <h3>Services Offered</h3>
              <div className="tags">
                {(lead.services_offered || []).map(s => <span key={s} className="tag">{s}</span>)}
              </div>
            </div>
            <div className="info-card">
              <h3>Competitors</h3>
              <div className="tags">
                {(lead.competitors || []).map(c => <span key={c} className="tag competitor">{c}</span>)}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'owner' && (
          <div className="owner-details">
            <div className="info-card full-width">
              <h3>Owner Profile</h3>
              <p className="owner-profile">{lead.owner_profile}</p>
            </div>
            <div className="info-card">
              <h3>Quick Contact</h3>
              <div className="contact-buttons">
                <a href={`mailto:${lead.email_primary}`} className="btn btn-primary">✉ Email</a>
                <a href={`tel:${lead.phone}`} className="btn btn-secondary">☎ Call</a>
                <a href={lead.website} target="_blank" rel="noreferrer" className="btn btn-secondary">🌐 Website</a>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'analysis' && (
          <div className="analysis-details">
            <div className="info-card full-width">
              <h3>Full Business Analysis</h3>
              <p className="analysis-text">{lead.full_analysis}</p>
            </div>
            <div className="info-card">
              <h3>Pain Points</h3>
              <div className="tags">
                {(lead.pain_points || []).map(p => <span key={p} className="tag pain">{p}</span>)}
              </div>
            </div>
            <div className="info-card">
              <h3>Review Summary</h3>
              <div className="info-row"><span>Current Rating:</span><strong>{lead.current_rating}/5</strong></div>
              <div className="info-row"><span>Negative Reviews:</span><span className="negative">{lead.negative_review_count}</span></div>
              <div className="platform-ratings">
                {Object.entries(lead.review_platforms || {}).map(([p, r]) => (
                  <div key={p} className="platform-rating">{p}: {r}</div>
                ))}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'interactions' && (
          <div className="interactions-details">
            <div className="info-card full-width">
              <h3>Interaction History</h3>
              {(lead.interaction_history || []).length === 0 ? (
                <p>No interactions yet</p>
              ) : (
                <div className="timeline">
                  {lead.interaction_history.map((interaction, i) => (
                    <div key={i} className={`timeline-item ${interaction.type}`}>
                      <div className="timeline-date">{interaction.date}</div>
                      <div className="timeline-type">{interaction.type.replace('_', ' ')}</div>
                      {interaction.subject && <div className="timeline-subject">Subject: {interaction.subject}</div>}
                      {interaction.result && <div className="timeline-result">Result: {interaction.result}</div>}
                      {interaction.content && <div className="timeline-content">"{interaction.content}"</div>}
                    </div>
                  ))}
                </div>
              )}
            </div>
            <div className="info-card">
              <h3>Email Stats</h3>
              <div className="info-row"><span>Emails Sent:</span><strong>{lead.emails_sent_count}</strong></div>
              <div className="info-row"><span>Last Contact:</span>{lead.last_contact}</div>
              <div className="info-row"><span>Status:</span><span className={`status-${lead.status}`}>{lead.status}</span></div>
            </div>
          </div>
        )}

        {activeTab === 'call-guide' && (
          <div className="call-guide">
            <div className="info-card full-width">
              <h3>📞 Call Script Notes</h3>
              <p className="call-script">{lead.call_script_notes}</p>
            </div>
            <div className="info-card">
              <h3>Quick Stats for Call</h3>
              <div className="info-row"><span>Lead Score:</span><strong>{lead.lead_score}</strong></div>
              <div className="info-row"><span>Closing Probability:</span><strong>{lead.closing_probability}%</strong></div>
              <div className="info-row"><span>Temperature:</span><span style={{ color: tempColor }}>{lead.lead_temperature}</span></div>
              <div className="info-row"><span>Pain Points:</span>{lead.pain_points?.join(', ')}</div>
            </div>
            <div className="info-card">
              <h3>Key Talking Points</h3>
              <ul className="talking-points">
                <li>Business: {lead.business_nature}</li>
                <li>Years: {lead.years_in_business} years in business</li>
                <li>Team: {lead.employee_count} employees</li>
                <li>Reviews: {lead.negative_review_count} negative reviews need removal</li>
              </ul>
            </div>
          </div>
        )}
      </div>

      <style>{`
        .lead-details-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; padding: 20px; background: var(--card-bg); border-radius: 12px; }
        .header-left h1 { margin: 0 0 10px 0; font-size: 28px; }
        .temperature-badge { padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: bold; color: white; margin-left: 10px; }
        .important-badge { background: #fbbf24; color: #000; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: bold; margin-left: 10px; }
        .header-right { display: flex; gap: 20px; }
        .score-display { text-align: center; background: var(--bg-secondary); padding: 10px 20px; border-radius: 8px; }
        .score-label { font-size: 12px; color: var(--text-secondary); }
        .score-value { font-size: 24px; font-weight: bold; color: var(--primary); }
        .tabs { display: flex; gap: 5px; margin-bottom: 20px; }
        .tabs button { padding: 10px 20px; border: none; background: var(--bg-secondary); cursor: pointer; border-radius: 8px 8px 0 0; }
        .tabs button.active { background: var(--primary); color: white; }
        .tab-content { background: var(--card-bg); padding: 20px; border-radius: 0 12px 12px 12px; }
        .overview-grid, .business-details, .analysis-details, .interactions-details, .call-guide { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
        .info-card { background: var(--bg-secondary); padding: 20px; border-radius: 8px; }
        .info-card.full-width { grid-column: 1 / -1; }
        .info-card h3 { margin: 0 0 15px 0; color: var(--primary); font-size: 16px; }
        .info-row { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid var(--border); }
        .info-row span { color: var(--text-secondary); }
        .info-row a { color: var(--primary); }
        .rating-bars { display: flex; flex-direction: column; gap: 8px; }
        .rating-bar { display: flex; align-items: center; gap: 10px; }
        .rating-bar .platform { width: 80px; font-size: 12px; }
        .rating-bar .bar { flex: 1; height: 8px; background: var(--border); border-radius: 4px; overflow: hidden; }
        .rating-bar .fill { height: 100%; background: var(--primary); }
        .rating-bar .value { width: 30px; text-align: right; }
        .tags { display: flex; flex-wrap: wrap; gap: 8px; }
        .tag { background: var(--primary); color: white; padding: 4px 12px; border-radius: 20px; font-size: 12px; }
        .tag.competitor { background: var(--accent); }
        .tag.pain { background: #ef4444; }
        .important-notes { border-left: 4px solid #fbbf24; background: #fef3c7; }
        .owner-profile { line-height: 1.8; color: var(--text); }
        .contact-buttons { display: flex; gap: 10px; flex-wrap: wrap; }
        .btn { padding: 10px 20px; border-radius: 8px; text-decoration: none; font-weight: bold; }
        .btn-primary { background: var(--primary); color: white; }
        .btn-secondary { background: var(--bg-primary); color: var(--text); border: 1px solid var(--border); }
        .analysis-text { line-height: 1.8; white-space: pre-line; }
        .negative { color: #ef4444; font-weight: bold; }
        .timeline { border-left: 3px solid var(--primary); padding-left: 20px; }
        .timeline-item { margin-bottom: 20px; position: relative; }
        .timeline-item::before { content: ''; width: 12px; height: 12px; background: var(--primary); border-radius: 50%; position: absolute; left: -27px; top: 4px; }
        .timeline-date { font-size: 12px; color: var(--text-secondary); }
        .timeline-type { font-weight: bold; text-transform: capitalize; }
        .call-script { font-size: 18px; line-height: 1.8; color: var(--text); background: #f0f9ff; padding: 20px; border-radius: 8px; }
        .talking-points li { padding: 8px 0; }
        .status-active { color: #22c55e; }
        .status-replied { color: #3b82f6; }
      `}</style>
    </div>
  );
}