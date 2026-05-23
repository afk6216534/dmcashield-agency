import { useState, useEffect } from 'react';
import API from '../config/api.js';

export default function AgentBrains() {
  const [brains, setBrains] = useState({});
  const [selected, setSelected] = useState(null);
  const [detail, setDetail] = useState(null);
  const [learning, setLearning] = useState(null);
  const [tab, setTab] = useState('brains'); // brains | learning | experiments
  const [runningCycle, setRunningCycle] = useState(false);

  useEffect(() => {
    fetch(`${API}/api/agents/brains`).then(r => r.json()).then(d => setBrains(d.agents || {})).catch(() => {});
    fetch(`${API}/api/learning/engine`).then(r => r.json()).then(d => setLearning(d)).catch(() => {});
  }, []);

  const viewBrain = async (name) => {
    setSelected(name);
    try {
      const r = await fetch(`${API}/api/agents/${name}/brain`);
      const d = await r.json();
      setDetail(d);
    } catch { setDetail(null); }
  };

  const runCycle = async () => {
    setRunningCycle(true);
    try {
      const r = await fetch(`${API}/api/learning/run-cycle`, { method: 'POST' });
      const d = await r.json();
      setLearning(prev => ({ ...prev, cycle: d.cycle }));
      // Refresh brains after learning
      const br = await fetch(`${API}/api/agents/brains`);
      const bd = await br.json();
      setBrains(bd.agents || {});
      if (selected) viewBrain(selected);
      alert(`✅ Learning cycle ${d.cycle} complete! ${d.improved_agents} agents improved.`);
    } catch { alert('Learning cycle failed'); }
    setRunningCycle(false);
  };

  const SkillBar = ({ name, level }) => (
    <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 6 }}>
      <span style={{ width: 150, fontSize: '0.82rem', color: 'var(--text-secondary)' }}>{name.replace(/_/g, ' ')}</span>
      <div style={{ flex: 1, height: 8, borderRadius: 4, background: 'var(--bg-tertiary)', overflow: 'hidden' }}>
        <div style={{ width: `${level}%`, height: '100%', borderRadius: 4,
          background: level >= 90 ? 'linear-gradient(90deg, #10b981, #34d399)' : level >= 80 ? 'linear-gradient(90deg, #3b82f6, #60a5fa)' : level >= 70 ? 'linear-gradient(90deg, #f59e0b, #fbbf24)' : 'linear-gradient(90deg, #ef4444, #f87171)',
          transition: 'width 0.6s ease' }} />
      </div>
      <span style={{ fontSize: '0.82rem', fontWeight: 600, color: level >= 90 ? '#10b981' : level >= 80 ? '#3b82f6' : '#f59e0b', minWidth: 30 }}>{level}%</span>
    </div>
  );

  return (
    <div style={{ padding: 24 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <div>
          <h1 style={{ fontSize: '1.8rem', fontWeight: 800, background: 'linear-gradient(135deg, #a855f7, #6366f1)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>🧠 Agent Brain System</h1>
          <p style={{ color: 'var(--text-secondary)', marginTop: 4 }}>24/7 Auto-Learning • Internet Intelligence • Skill Progression</p>
        </div>
        <button onClick={runCycle} disabled={runningCycle}
          style={{ padding: '10px 20px', borderRadius: 8, border: 'none', cursor: 'pointer',
            background: runningCycle ? 'var(--bg-tertiary)' : 'linear-gradient(135deg, #a855f7, #6366f1)', color: '#fff', fontWeight: 600, fontSize: '0.9rem' }}>
          {runningCycle ? '⏳ Learning...' : '⚡ Run Learning Cycle'}
        </button>
      </div>

      {/* Tab bar */}
      <div style={{ display: 'flex', gap: 8, marginBottom: 20 }}>
        {[['brains', '🧠 Agent Brains'], ['learning', '📚 Auto-Learning'], ['experiments', '🧪 Experiments']].map(([key, label]) => (
          <button key={key} onClick={() => setTab(key)}
            style={{ padding: '8px 16px', borderRadius: 8, border: 'none', cursor: 'pointer',
              background: tab === key ? 'var(--accent)' : 'var(--bg-secondary)', color: tab === key ? '#fff' : 'var(--text-secondary)', fontWeight: 600, fontSize: '0.85rem' }}>
            {label}
          </button>
        ))}
      </div>

      {tab === 'brains' && (
        <div style={{ display: 'flex', gap: 20 }}>
          {/* Agent list */}
          <div style={{ width: 300, display: 'flex', flexDirection: 'column', gap: 6 }}>
            {Object.entries(brains).sort((a, b) => b[1].avg_skill_level - a[1].avg_skill_level).map(([name, brain]) => (
              <div key={name} onClick={() => viewBrain(name)}
                style={{ padding: '12px 14px', borderRadius: 10, cursor: 'pointer',
                  background: selected === name ? 'var(--accent)' : 'var(--bg-secondary)',
                  color: selected === name ? '#fff' : 'inherit', borderLeft: `3px solid ${brain.avg_skill_level >= 90 ? '#10b981' : brain.avg_skill_level >= 85 ? '#3b82f6' : '#f59e0b'}` }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <strong style={{ fontSize: '0.9rem' }}>{brain.role === 'head' ? '👔' : '🤖'} {name}</strong>
                  <span style={{ fontSize: '0.78rem', padding: '2px 8px', borderRadius: 12, background: 'rgba(255,255,255,0.1)' }}>{brain.avg_skill_level}%</span>
                </div>
                <div style={{ fontSize: '0.78rem', opacity: 0.7, marginTop: 2 }}>{brain.department} • {brain.skill_count} skills • {brain.personality}</div>
              </div>
            ))}
          </div>

          {/* Brain detail */}
          <div style={{ flex: 1 }}>
            {detail ? (
              <div style={{ background: 'var(--bg-secondary)', borderRadius: 12, padding: 24 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }}>
                  <div>
                    <h2 style={{ fontSize: '1.4rem', fontWeight: 700, marginBottom: 4 }}>{detail.role === 'head' ? '👔' : '🤖'} {detail.agent}</h2>
                    <p style={{ color: 'var(--text-secondary)' }}>{detail.department} department • {detail.role}</p>
                  </div>
                  {detail.personality?.catchphrase && (
                    <div style={{ padding: '8px 14px', borderRadius: 8, background: 'var(--bg-tertiary)', fontStyle: 'italic', fontSize: '0.85rem', maxWidth: 280 }}>
                      "{detail.personality.catchphrase}"
                    </div>
                  )}
                </div>

                {/* Personality */}
                {detail.personality?.traits && (
                  <div style={{ display: 'flex', gap: 8, marginBottom: 20, flexWrap: 'wrap' }}>
                    <span style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', paddingTop: 3 }}>Traits:</span>
                    {detail.personality.traits.map(t => (
                      <span key={t} style={{ padding: '4px 10px', borderRadius: 12, background: 'var(--bg-tertiary)', fontSize: '0.8rem' }}>{t}</span>
                    ))}
                  </div>
                )}

                {/* Stats row */}
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 12, marginBottom: 24 }}>
                  <div style={{ padding: 14, borderRadius: 8, background: 'var(--bg-tertiary)', textAlign: 'center' }}>
                    <div style={{ fontSize: '1.5rem', fontWeight: 800, color: '#10b981' }}>{Object.keys(detail.skills || {}).length}</div>
                    <div style={{ fontSize: '0.78rem', color: 'var(--text-secondary)' }}>Skills</div>
                  </div>
                  <div style={{ padding: 14, borderRadius: 8, background: 'var(--bg-tertiary)', textAlign: 'center' }}>
                    <div style={{ fontSize: '1.5rem', fontWeight: 800, color: '#3b82f6' }}>{detail.total_experience}</div>
                    <div style={{ fontSize: '0.78rem', color: 'var(--text-secondary)' }}>Tasks Done</div>
                  </div>
                  <div style={{ padding: 14, borderRadius: 8, background: 'var(--bg-tertiary)', textAlign: 'center' }}>
                    <div style={{ fontSize: '1.5rem', fontWeight: 800, color: '#a855f7' }}>
                      {Object.values(detail.skills || {}).length > 0 ? Math.round(Object.values(detail.skills).reduce((a, b) => a + b, 0) / Object.values(detail.skills).length) : 0}%
                    </div>
                    <div style={{ fontSize: '0.78rem', color: 'var(--text-secondary)' }}>Avg Skill</div>
                  </div>
                </div>

                {/* Skills with progress bars */}
                <h3 style={{ marginBottom: 12, fontSize: '1rem', fontWeight: 700 }}>📊 Skill Levels</h3>
                {Object.entries(detail.skills || {}).sort((a, b) => b[1] - a[1]).map(([skill, level]) => (
                  <SkillBar key={skill} name={skill} level={level} />
                ))}
              </div>
            ) : (
              <div style={{ textAlign: 'center', padding: 60, color: 'var(--text-secondary)' }}>
                <div style={{ fontSize: '3rem', marginBottom: 12 }}>🧠</div>
                <p>Select an agent to view their brain</p>
              </div>
            )}
          </div>
        </div>
      )}

      {tab === 'learning' && learning && (
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20 }}>
          {/* Engine status */}
          <div style={{ background: 'var(--bg-secondary)', borderRadius: 12, padding: 24 }}>
            <h3 style={{ marginBottom: 16, fontSize: '1.1rem', fontWeight: 700 }}>🤖 Learning Engine Status</h3>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
              <div style={{ padding: 14, borderRadius: 8, background: 'var(--bg-tertiary)', textAlign: 'center' }}>
                <div style={{ fontSize: '1.8rem', fontWeight: 800, color: '#10b981' }}>🟢</div>
                <div style={{ fontSize: '0.85rem', fontWeight: 600 }}>{learning.engine_status?.toUpperCase()}</div>
              </div>
              <div style={{ padding: 14, borderRadius: 8, background: 'var(--bg-tertiary)', textAlign: 'center' }}>
                <div style={{ fontSize: '1.5rem', fontWeight: 800, color: '#3b82f6' }}>{learning.cycle}</div>
                <div style={{ fontSize: '0.78rem', color: 'var(--text-secondary)' }}>Learning Cycles</div>
              </div>
              <div style={{ padding: 14, borderRadius: 8, background: 'var(--bg-tertiary)', textAlign: 'center' }}>
                <div style={{ fontSize: '1.5rem', fontWeight: 800, color: '#a855f7' }}>{learning.total_learnings}</div>
                <div style={{ fontSize: '0.78rem', color: 'var(--text-secondary)' }}>Total Learnings</div>
              </div>
              <div style={{ padding: 14, borderRadius: 8, background: 'var(--bg-tertiary)', textAlign: 'center' }}>
                <div style={{ fontSize: '1.5rem', fontWeight: 800, color: '#f59e0b' }}>{learning.next_cycle}</div>
                <div style={{ fontSize: '0.78rem', color: 'var(--text-secondary)' }}>Next Cycle</div>
              </div>
            </div>

            <h4 style={{ margin: '20px 0 12px', fontWeight: 600 }}>📈 Skill Improvements</h4>
            {(learning.skill_improvements || []).map((imp, i) => (
              <div key={i} style={{ padding: 10, borderRadius: 8, background: 'var(--bg-tertiary)', marginBottom: 6, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                  <strong style={{ fontSize: '0.85rem' }}>{imp.agent}</strong>
                  <div style={{ fontSize: '0.78rem', color: 'var(--text-secondary)' }}>{imp.skill.replace(/_/g, ' ')}</div>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                  <span style={{ color: '#ef4444', fontSize: '0.85rem' }}>{imp.from}%</span>
                  <span>→</span>
                  <span style={{ color: '#10b981', fontWeight: 700, fontSize: '0.85rem' }}>{imp.to}%</span>
                </div>
              </div>
            ))}
          </div>

          {/* Discoveries */}
          <div>
            <div style={{ background: 'var(--bg-secondary)', borderRadius: 12, padding: 24, marginBottom: 20 }}>
              <h3 style={{ marginBottom: 16, fontSize: '1.1rem', fontWeight: 700 }}>💡 AI Discoveries</h3>
              {(learning.discoveries || []).map(d => (
                <div key={d.id} style={{ padding: 12, borderRadius: 8, background: 'var(--bg-tertiary)', marginBottom: 8, borderLeft: `3px solid ${d.confidence >= 90 ? '#10b981' : d.confidence >= 80 ? '#3b82f6' : '#f59e0b'}` }}>
                  <div style={{ fontSize: '0.88rem', fontWeight: 600, marginBottom: 4 }}>{d.discovery}</div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.76rem', color: 'var(--text-secondary)' }}>
                    <span>📗 {d.source}</span>
                    <span style={{ color: d.confidence >= 90 ? '#10b981' : '#3b82f6' }}>Confidence: {d.confidence}%</span>
                  </div>
                </div>
              ))}
            </div>

            <div style={{ background: 'var(--bg-secondary)', borderRadius: 12, padding: 24 }}>
              <h3 style={{ marginBottom: 16, fontSize: '1.1rem', fontWeight: 700 }}>🌐 Internet Sources (24/7)</h3>
              {(learning.internet_sources || []).map((s, i) => (
                <div key={i} style={{ padding: 10, borderRadius: 8, background: 'var(--bg-tertiary)', marginBottom: 6, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <div>
                    <div style={{ fontSize: '0.85rem', fontWeight: 600 }}>{s.source}</div>
                    <div style={{ fontSize: '0.76rem', color: 'var(--text-secondary)' }}>{s.topic}</div>
                  </div>
                  <span style={{ fontSize: '0.76rem', color: 'var(--text-secondary)' }}>🕐 {s.last_checked}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {tab === 'experiments' && learning && (
        <div style={{ background: 'var(--bg-secondary)', borderRadius: 12, padding: 24 }}>
          <h3 style={{ marginBottom: 16, fontSize: '1.1rem', fontWeight: 700 }}>🧪 Active Experiments</h3>
          {(learning.active_experiments || []).map(exp => (
            <div key={exp.id} style={{ padding: 16, borderRadius: 10, background: 'var(--bg-tertiary)', marginBottom: 12, borderLeft: `3px solid ${exp.status === 'completed' ? '#10b981' : '#3b82f6'}` }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
                <strong style={{ fontSize: '1rem' }}>{exp.name}</strong>
                <span style={{ padding: '3px 10px', borderRadius: 12, fontSize: '0.78rem',
                  background: exp.status === 'completed' ? 'rgba(16,185,129,0.2)' : 'rgba(59,130,246,0.2)',
                  color: exp.status === 'completed' ? '#10b981' : '#3b82f6' }}>{exp.status.toUpperCase()}</span>
              </div>
              <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>Department: {exp.department} • Started: {exp.started}</div>
              <div style={{ marginTop: 8, padding: 8, borderRadius: 6, background: 'rgba(168,85,247,0.1)', fontSize: '0.85rem' }}>
                📊 Results: <strong>{exp.results_so_far}</strong>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
