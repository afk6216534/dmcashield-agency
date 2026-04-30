import { useState, useEffect } from 'react';
const API = 'http://localhost:8000';

export default function SelfLearning() {
  const [data, setData] = useState({
    patterns_learned: 12,
    campaigns_optimized: 8,
    subject_lines_improved: 23,
    send_times_optimized: 5,
    avg_open_rate_improvement: 15,
    avg_reply_rate_improvement: 8
  });

  const [recentLearning, setRecentLearning] = useState([
    { date: 'Today', pattern: 'Subject lines with "?" get 20% more opens', type: 'subject' },
    { date: 'Today', pattern: 'Tuesday 9AM is best send time', type: 'timing' },
    { date: 'Yesterday', pattern: 'Personalized emails 3x more replies', type: 'personalization' },
    { date: 'Yesterday', pattern: 'Keep subject under 40 chars', type: 'subject' },
    { date: 'Apr 28', pattern: 'Pizza shops reply faster', type: 'industry' },
  ]);

  const [optimizations, setOptimizations] = useState([
    { name: 'Subject Line Strategy', status: 'active', improvement: '+15%' },
    { name: 'Send Time Optimization', status: 'active', improvement: '+8%' },
    { name: 'Personalization Engine', status: 'active', improvement: '+23%' },
    { name: 'Industry Targeting', status: 'learning', improvement: '+5%' },
  ]);

  const learningSources = [
    { source: 'Email Opens', count: 1247 },
    { source: 'Email Clicks', count: 389 },
    { source: 'Replies', count: 87 },
    { source: 'Bounces', count: 12 },
  ];

  return (
    <div className="main-content animate-in">
      <div className="page-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <div>
          <h1>🧠 Self-Learning AI</h1>
          <p>Continuous learning and optimization from every campaign</p>
        </div>
        <div style={{ display: 'flex', gap: 8 }}>
          <span className="badge badge-active">🟢 Learning Active</span>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="stats-grid">
        <div className="stat-card purple">
          <div className="stat-label">Patterns Learned</div>
          <div className="stat-value purple">{data.patterns_learned}</div>
        </div>
        <div className="stat-card teal">
          <div className="stat-label">Campaigns Optimized</div>
          <div className="stat-value teal">{data.campaigns_optimized}</div>
        </div>
        <div className="stat-card green">
          <div className="stat-label">Open Rate Improved</div>
          <div className="stat-value green">+{data.avg_open_rate_improvement}%</div>
        </div>
        <div className="stat-card orange">
          <div className="stat-label">Reply Rate Improved</div>
          <div className="stat-value orange">+{data.avg_reply_rate_improvement}%</div>
        </div>
      </div>

      {/* Recent Learning */}
      <div className="glass-card no-hover" style={{ marginBottom: 20 }}>
        <h3 style={{ marginBottom: 16 }}>📚 Recent Learning</h3>
        {recentLearning.map((item, i) => (
          <div key={i} style={{ padding: '10px 0', borderBottom: '1px solid var(--border-subtle)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div>
              <span style={{ fontSize: '0.72rem', color: 'var(--text-tertiary)', marginRight: 8 }}>{item.date}</span>
              <span style={{ color: 'var(--text-secondary)' }}>{item.pattern}</span>
            </div>
            <span className="badge" style={{ background: item.type === 'subject' ? 'var(--accent-primary)' : item.type === 'timing' ? 'var(--accent-secondary)' : 'var(--accent-warning)', fontSize: '0.68rem' }}>
              {item.type}
            </span>
          </div>
        ))}
      </div>

      {/* Optimizations */}
      <div className="grid-2">
        <div className="glass-card no-hover">
          <h3 style={{ marginBottom: 16 }}>⚙️ Active Optimizations</h3>
          {optimizations.map((opt, i) => (
            <div key={i} style={{ padding: '12px', background: 'var(--bg-tertiary)', borderRadius: 10, marginBottom: 8 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 4 }}>
                <span style={{ fontWeight: 600, fontSize: '0.86rem' }}>{opt.name}</span>
                <span style={{ color: 'var(--accent-success)', fontWeight: 600, fontSize: '0.86rem' }}>{opt.improvement}</span>
              </div>
              <span className={`badge ${opt.status === 'active' ? 'badge-active' : 'badge-warm'}`}>{opt.status}</span>
            </div>
          ))}
        </div>

        <div className="glass-card no-hover">
          <h3 style={{ marginBottom: 16 }}>📊 Learning Sources</h3>
          {learningSources.map((src, i) => (
            <div key={i} style={{ padding: '8px 0', borderBottom: '1px solid var(--border-subtle)', display: 'flex', justifyContent: 'space-between' }}>
              <span style={{ color: 'var(--text-secondary)' }}>{src.source}</span>
              <span style={{ color: 'var(--text-primary)', fontWeight: 600 }}>{src.count.toLocaleString()}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Learning Settings */}
      <div className="glass-card no-hover" style={{ marginTop: 20 }}>
        <h3 style={{ marginBottom: 16 }}>⚙️ Learning Settings</h3>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 16 }}>
          <div className="form-group">
            <label className="form-label">Learning Rate</label>
            <select className="form-input" defaultValue="0.05">
              <option value="0.01">Slow (0.01)</option>
              <option value="0.05">Normal (0.05)</option>
              <option value="0.1">Fast (0.1)</option>
            </select>
          </div>
          <div className="form-group">
            <label className="form-label">Feedback Required</label>
            <select className="form-input" defaultValue="10">
              <option value="5">5 samples</option>
              <option value="10">10 samples</option>
              <option value="20">20 samples</option>
            </select>
          </div>
          <div className="form-group">
            <label className="form-label">Auto-Apply</label>
            <select className="form-input" defaultValue="true">
              <option value="true">Yes - Apply automatically</option>
              <option value="false">No - Ask first</option>
            </select>
          </div>
        </div>
        <button className="btn btn-primary">Save Settings</button>
      </div>
    </div>
  );
}