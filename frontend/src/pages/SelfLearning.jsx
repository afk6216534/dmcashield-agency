import { useState, useEffect } from 'react';
import API from '../config/api.js';

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

  const [improvementPlan, setImprovementPlan] = useState({ issues: [], success_rate: 0, total_improvements: 0, pending_issues: 0 });
  const [mistakeCategory, setMistakeCategory] = useState('sales');
  const [mistakeContext, setMistakeContext] = useState('');
  const [mistakeReason, setMistakeReason] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const learningSources = [
    { source: 'Email Opens', count: 1247 },
    { source: 'Email Clicks', count: 389 },
    { source: 'Replies', count: 87 },
    { source: 'Bounces', count: 12 },
  ];

  // Fetch improvement plan on mount
  useEffect(() => {
    fetch(`${API}/api/ai/improvement-plan`)
      .then(res => res.json())
      .then(data => setImprovementPlan(data))
      .catch(err => console.error('Failed to load improvement plan:', err));
  }, []);

  // Handler for mistake submission
  const handleMistakeSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    try {
      const response = await fetch(`${API}/api/ai/learn-from-mistakes`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          category: mistakeCategory,
          context: { description: mistakeContext },
          reason: mistakeReason
        })
      });
      if (response.ok) {
        // Refresh improvement plan
        const planRes = await fetch(`${API}/api/ai/improvement-plan`);
        const planData = await planRes.json();
        setImprovementPlan(planData);
        // Clear form
        setMistakeContext('');
        setMistakeReason('');
        alert('Mistake reported successfully!');
      }
    } catch (error) {
      console.error('Failed to report mistake:', error);
    }
    setIsSubmitting(false);
  };

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

      {/* Mistake Tracker & Improvement Plan */}
      <div className="glass-card no-hover" style={{ marginTop: 20 }}>
        <h3 style={{ marginBottom: 16 }}>🚨 AI Mistake Tracker & Improvement Plan</h3>

        {/* Mistake Reporting Form */}
        <div style={{ background: 'var(--bg-tertiary)', padding: '16px', borderRadius: '10px', marginBottom: '16px' }}>
          <form onSubmit={handleMistakeSubmit} style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
            <div>
              <label className="form-label">Mistake Category</label>
              <select
                className="form-input"
                value={mistakeCategory}
                onChange={(e) => setMistakeCategory(e.target.value)}
                required
              >
                <option value="sales">Sales Process</option>
                <option value="marketing">Marketing Campaign</option>
                <option value="email">Email Performance</option>
                <option value="general">Other</option>
              </select>
            </div>

            <div style={{ gridColumn: '1 / -1' }}>
              <label className="form-label">Context / Situation</label>
              <textarea
                className="form-input"
                value={mistakeContext}
                onChange={(e) => setMistakeContext(e.target.value)}
                placeholder="Describe what happened when the mistake occurred..."
                rows="3"
                required
              />
            </div>

            <div style={{ gridColumn: '1 / -1' }}>
              <label className="form-label">What Went Wrong?</label>
              <textarea
                className="form-input"
                value={mistakeReason}
                onChange={(e) => setMistakeReason(e.target.value)}
                placeholder="Explain the failure or error..."
                rows="3"
                required
              />
            </div>

            <div style={{ gridColumn: '1 / -1', textAlign: 'right' }}>
              <button
                type="submit"
                className="btn btn-primary"
                disabled={isSubmitting}
              >
                {isSubmitting ? 'Reporting...' : 'Report Mistake'}
              </button>
            </div>
          </form>
        </div>

        {/* Improvement Plan Display */}
        <div style={{ background: 'var(--bg-tertiary)', padding: '16px', borderRadius: '10px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
            <h4 style={{ margin: 0 }}>📊 Current Improvement Plan</h4>
            <span className="badge" style={{ background: 'var(--accent-secondary)' }}>
              {improvementPlan.pending_issues} Pending Issues
            </span>
          </div>

          {improvementPlan.issues.length > 0 ? (
            <div>
              {improvementPlan.issues.map((issue, index) => (
                <div key={index} style={{ padding: '10px', marginBottom: '8px', background: 'var(--bg-secondary)', borderRadius: '8px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px' }}>
                    <strong style={{ color: 'var(--text-primary)' }}>{issue.category}</strong>
                    <span className={`badge ${issue.priority === 'high' ? 'badge-warm' : 'badge-active'}`}>
                      {issue.priority}
                    </span>
                  </div>
                  <p style={{ margin: 0, color: 'var(--text-secondary)', fontSize: '0.86rem' }}>
                    {issue.suggestion}
                  </p>
                </div>
              ))}

              <div style={{ marginTop: '12px', paddingTop: '8px', borderTop: '1px solid var(--border-subtle)', textAlign: 'center', fontSize: '0.86rem', color: 'var(--accent-success)' }}>
                Success Rate: {Math.round(improvementPlan.success_rate * 100)}% •
                {improvementPlan.total_improvements} Improvements Applied
              </div>
            </div>
          ) : (
            <div style={{ textAlign: 'center', padding: '20px', color: 'var(--text-tertiary)' }}>
              No improvement suggestions yet. Report mistakes to generate AI-powered insights!
            </div>
          )}
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
