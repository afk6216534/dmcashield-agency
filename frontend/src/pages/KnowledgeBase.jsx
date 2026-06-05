import { useState, useEffect } from 'react';
import API from '../config/api.js';

export default function KnowledgeBase() {
  const [knowledge, setKnowledge] = useState(null);
  const [coldEmail, setColdEmail] = useState(null);
  const [psychology, setPsychology] = useState(null);
  const [agents, setAgents] = useState(null);
  const [workflows, setWorkflows] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState(null);
  const [tab, setTab] = useState('overview');

  useEffect(() => {
    Promise.all([
      fetch(`${API}/api/knowledge`).then(r => r.json()).catch(() => null),
      fetch(`${API}/api/knowledge/cold-email`).then(r => r.json()).catch(() => null),
      fetch(`${API}/api/knowledge/psychology`).then(r => r.json()).catch(() => null),
      fetch(`${API}/api/knowledge/agents`).then(r => r.json()).catch(() => null),
      fetch(`${API}/api/knowledge/workflows`).then(r => r.json()).catch(() => null),
    ]).then(([k, c, p, a, w]) => { 
      setKnowledge(k); 
      setColdEmail(c); 
      setPsychology(p); 
      setAgents(a); 
      setWorkflows(w);
    });
  }, []);

  const handleSearch = async () => {
    if (!searchQuery.trim()) return;
    try {
      const r = await fetch(`${API}/api/knowledge/search?q=${encodeURIComponent(searchQuery)}`);
      setSearchResults(await r.json());
    } catch { setSearchResults({ results: [], count: 0 }); }
  };

  const statusColors = { integrated: '#10b981', referenced: '#3b82f6', 'design-referenced': '#a855f7' };
  const categoryColors = { cold_email: '#ef4444', psychology: '#a855f7', marketing_skill: '#3b82f6' };

  return (
    <div style={{ padding: 24 }}>
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <div>
          <h1 style={{ fontSize: '1.8rem', fontWeight: 800, background: 'linear-gradient(135deg, #f59e0b, #ef4444)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>📚 Knowledge Base</h1>
          <p style={{ color: 'var(--text-secondary)', marginTop: 4 }}>
            {knowledge?.repos_integrated || 41} repos integrated • {knowledge?.skills_loaded || 38} marketing skills • AI-powered search
          </p>
        </div>
      </div>

      {/* Search bar */}
      <div style={{ display: 'flex', gap: 8, marginBottom: 20 }}>
        <input value={searchQuery} onChange={e => setSearchQuery(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && handleSearch()}
          placeholder="Search knowledge... (e.g., 'cold email', 'loss aversion', 'funnel')"
          style={{ flex: 1, padding: '10px 16px', borderRadius: 8, border: '1px solid var(--bg-tertiary)', background: 'var(--bg-secondary)', color: 'inherit', fontSize: '0.9rem' }} />
        <button onClick={handleSearch}
          style={{ padding: '10px 20px', borderRadius: 8, border: 'none', cursor: 'pointer', background: 'linear-gradient(135deg, #f59e0b, #ef4444)', color: '#fff', fontWeight: 600 }}>
          🔍 Search
        </button>
      </div>

      {/* Search results */}
      {searchResults && (
        <div style={{ background: 'var(--bg-secondary)', borderRadius: 12, padding: 20, marginBottom: 20 }}>
          <h3 style={{ marginBottom: 12, fontSize: '1rem', fontWeight: 700 }}>
            🔍 "{searchResults.query}" — {searchResults.count} results
          </h3>
          {searchResults.results.length === 0 ? (
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem' }}>No results found. Try: "email", "proof", "scarcity", "funnel"</p>
          ) : (
            searchResults.results.map((r, i) => (
              <div key={i} style={{ padding: '10px 14px', borderRadius: 8, background: 'var(--bg-tertiary)', marginBottom: 6, borderLeft: `3px solid ${categoryColors[r.category] || '#6b7280'}` }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 2 }}>
                  <span style={{ fontSize: '0.85rem', fontWeight: 600 }}>{r.content}</span>
                  <span style={{ fontSize: '0.68rem', padding: '2px 8px', borderRadius: 8, background: `${categoryColors[r.category]}22`, color: categoryColors[r.category] }}>{r.category}</span>
                </div>
              </div>
            ))
          )}
        </div>
      )}

      {/* Tab bar */}
      <div style={{ display: 'flex', gap: 8, marginBottom: 20 }}>
        {[
          ['overview', '📊 Repos Overview'],
          ['cold-email', '📧 Cold Email'],
          ['psychology', '🧠 Psychology'],
          ['agents', '🤖 Agent Patterns'],
          ['workflows', '⚙️ Workflows']
        ].map(([key, label]) => (
          <button key={key} onClick={() => setTab(key)}
            style={{ padding: '8px 16px', borderRadius: 8, border: 'none', cursor: 'pointer',
              background: tab === key ? 'var(--accent)' : 'var(--bg-secondary)', color: tab === key ? '#fff' : 'var(--text-secondary)', fontWeight: 600, fontSize: '0.85rem' }}>
            {label}
          </button>
        ))}
      </div>

      {/* Overview tab */}
      {tab === 'overview' && knowledge && (
        <div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 12, marginBottom: 20 }}>
            <div style={{ padding: 20, borderRadius: 12, background: 'var(--bg-secondary)', textAlign: 'center', borderBottom: '3px solid #f59e0b' }}>
              <div style={{ fontSize: '2.2rem', fontWeight: 800, color: '#f59e0b' }}>{knowledge.repos_integrated}</div>
              <div style={{ fontSize: '0.82rem', color: 'var(--text-secondary)' }}>Repos Integrated</div>
            </div>
            <div style={{ padding: 20, borderRadius: 12, background: 'var(--bg-secondary)', textAlign: 'center', borderBottom: '3px solid #3b82f6' }}>
              <div style={{ fontSize: '2.2rem', fontWeight: 800, color: '#3b82f6' }}>{knowledge.skills_loaded}</div>
              <div style={{ fontSize: '0.82rem', color: 'var(--text-secondary)' }}>Marketing Skills</div>
            </div>
            <div style={{ padding: 20, borderRadius: 12, background: 'var(--bg-secondary)', textAlign: 'center', borderBottom: '3px solid #10b981' }}>
              <div style={{ fontSize: '2.2rem', fontWeight: 800, color: '#10b981' }}>{Object.values(knowledge.sources).filter(s => s.status === 'integrated').length}</div>
              <div style={{ fontSize: '0.82rem', color: 'var(--text-secondary)' }}>Fully Integrated</div>
            </div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
            {Object.entries(knowledge.sources).map(([key, src]) => (
              <div key={key} style={{ padding: 16, borderRadius: 12, background: 'var(--bg-secondary)', borderLeft: `3px solid ${statusColors[src.status] || '#6b7280'}` }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
                  <strong style={{ fontSize: '0.92rem', textTransform: 'capitalize' }}>{key.replace(/_/g, ' ')}</strong>
                  <span style={{ fontSize: '0.68rem', padding: '2px 8px', borderRadius: 8, background: `${statusColors[src.status]}22`, color: statusColors[src.status] }}>{src.status}</span>
                </div>
                <div style={{ fontSize: '0.78rem', color: 'var(--text-secondary)', marginBottom: 6 }}>📦 {src.repo}</div>
                {src.skills && <div style={{ fontSize: '0.78rem', color: '#f59e0b' }}>📚 {src.skills} skills</div>}
                {src.patterns && typeof src.patterns === 'number' && <div style={{ fontSize: '0.78rem', color: '#a855f7' }}>🔧 {src.patterns} patterns</div>}
                {src.agents_studied && <div style={{ fontSize: '0.78rem', color: '#3b82f6' }}>🤖 {src.agents_studied} agents studied</div>}
                {src.components && <div style={{ fontSize: '0.78rem', color: '#10b981' }}>🎨 {src.components} components</div>}
                {src.techniques && <div style={{ fontSize: '0.78rem', color: '#ef4444' }}>🧠 {src.techniques} techniques</div>}
                {src.features && Array.isArray(src.features) && (
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: 4, marginTop: 6 }}>
                    {src.features.map(f => (
                      <span key={f} style={{ padding: '2px 8px', borderRadius: 8, fontSize: '0.68rem', background: 'var(--bg-tertiary)' }}>{f}</span>
                    ))}
                  </div>
                )}
                {src.categories && Array.isArray(src.categories) && (
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: 4, marginTop: 6 }}>
                    {src.categories.slice(0, 8).map(c => (
                      <span key={c} style={{ padding: '2px 8px', borderRadius: 8, fontSize: '0.68rem', background: 'var(--bg-tertiary)' }}>{c}</span>
                    ))}
                    {src.categories.length > 8 && <span style={{ padding: '2px 8px', borderRadius: 8, fontSize: '0.68rem', background: 'var(--bg-tertiary)', color: 'var(--accent)' }}>+{src.categories.length - 8} more</span>}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Cold Email tab */}
      {tab === 'cold-email' && coldEmail && (
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20 }}>
          <div>
            <div style={{ background: 'var(--bg-secondary)', borderRadius: 12, padding: 20, marginBottom: 16 }}>
              <h3 style={{ marginBottom: 12, fontWeight: 700 }}>📧 Cold Email Principles</h3>
              {coldEmail.principles.map((p, i) => (
                <div key={i} style={{ padding: '8px 12px', borderRadius: 8, background: 'var(--bg-tertiary)', marginBottom: 6, fontSize: '0.85rem', borderLeft: '3px solid #10b981' }}>
                  ✅ {p}
                </div>
              ))}
            </div>
            <div style={{ background: 'var(--bg-secondary)', borderRadius: 12, padding: 20 }}>
              <h3 style={{ marginBottom: 12, fontWeight: 700 }}>✉️ Subject Line Rules</h3>
              {coldEmail.subject_line_rules.map((r, i) => (
                <div key={i} style={{ padding: '8px 12px', borderRadius: 8, background: 'var(--bg-tertiary)', marginBottom: 6, fontSize: '0.85rem', borderLeft: '3px solid #3b82f6' }}>
                  📝 {r}
                </div>
              ))}
            </div>
          </div>
          <div>
            <div style={{ background: 'var(--bg-secondary)', borderRadius: 12, padding: 20, marginBottom: 16 }}>
              <h3 style={{ marginBottom: 12, fontWeight: 700 }}>🔧 Email Frameworks</h3>
              {coldEmail.frameworks.map((f, i) => (
                <div key={i} style={{ padding: 12, borderRadius: 8, background: 'var(--bg-tertiary)', marginBottom: 8, borderLeft: '3px solid #a855f7' }}>
                  <div style={{ fontSize: '0.88rem', fontWeight: 700, marginBottom: 4 }}>{f.name}</div>
                  <div style={{ fontSize: '0.78rem', color: 'var(--text-secondary)' }}>{f.desc}</div>
                </div>
              ))}
            </div>
            <div style={{ background: 'var(--bg-secondary)', borderRadius: 12, padding: 20 }}>
              <h3 style={{ marginBottom: 12, fontWeight: 700, color: '#ef4444' }}>🚫 Anti-Patterns (Never Do)</h3>
              {coldEmail.anti_patterns.map((a, i) => (
                <div key={i} style={{ padding: '8px 12px', borderRadius: 8, background: 'var(--bg-tertiary)', marginBottom: 6, fontSize: '0.85rem', borderLeft: '3px solid #ef4444' }}>
                  ❌ {a}
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Psychology tab */}
      {tab === 'psychology' && psychology && (
        <div>
          <div style={{ background: 'var(--bg-secondary)', borderRadius: 12, padding: 20, marginBottom: 16 }}>
            <h3 style={{ marginBottom: 16, fontWeight: 700 }}>🧠 Persuasion Principles (10 Core)</h3>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 10 }}>
              {psychology.persuasion_principles.map((p, i) => (
                <div key={i} style={{ padding: 14, borderRadius: 10, background: 'var(--bg-tertiary)', borderLeft: `3px solid ${['#ef4444','#3b82f6','#f59e0b','#10b981','#a855f7','#ec4899','#14b8a6','#f97316','#8b5cf6','#06b6d4'][i]}` }}>
                  <div style={{ fontSize: '0.92rem', fontWeight: 700, marginBottom: 4 }}>{p.name}</div>
                  <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>{p.rule}</div>
                </div>
              ))}
            </div>
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
            <div style={{ background: 'var(--bg-secondary)', borderRadius: 12, padding: 20 }}>
              <h3 style={{ marginBottom: 12, fontWeight: 700 }}>💰 Pricing Psychology</h3>
              {psychology.pricing_psychology.map((p, i) => (
                <div key={i} style={{ padding: '8px 12px', borderRadius: 8, background: 'var(--bg-tertiary)', marginBottom: 6, fontSize: '0.82rem', borderLeft: '3px solid #f59e0b' }}>
                  💡 {p}
                </div>
              ))}
            </div>
            <div style={{ background: 'var(--bg-secondary)', borderRadius: 12, padding: 20 }}>
              <h3 style={{ marginBottom: 12, fontWeight: 700 }}>📊 Funnel Psychology</h3>
              {psychology.funnel_psychology.map((p, i) => (
                <div key={i} style={{ padding: '8px 12px', borderRadius: 8, background: 'var(--bg-tertiary)', marginBottom: 6, fontSize: '0.82rem', borderLeft: '3px solid #3b82f6' }}>
                  🔬 {p}
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Agent Patterns tab */}
      {tab === 'agents' && agents && (
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20 }}>
          <div style={{ background: 'var(--bg-secondary)', borderRadius: 12, padding: 20 }}>
            <h3 style={{ marginBottom: 14, fontWeight: 700 }}>🔄 Orchestration Patterns</h3>
            <p style={{ fontSize: '0.78rem', color: 'var(--text-secondary)', marginBottom: 12 }}>From: {agents.source}</p>
            {agents.orchestration.map((p, i) => (
              <div key={i} style={{ padding: 12, borderRadius: 8, background: 'var(--bg-tertiary)', marginBottom: 8, borderLeft: '3px solid #10b981' }}>
                <div style={{ fontSize: '0.85rem', fontWeight: 600 }}>{p.split(':')[0]}</div>
                {p.includes(':') && <div style={{ fontSize: '0.78rem', color: 'var(--text-secondary)', marginTop: 2 }}>{p.split(':').slice(1).join(':').trim()}</div>}
              </div>
            ))}
          </div>
          <div style={{ background: 'var(--bg-secondary)', borderRadius: 12, padding: 20 }}>
            <h3 style={{ marginBottom: 14, fontWeight: 700 }}>💬 Communication Patterns</h3>
            {agents.communication.map((p, i) => (
              <div key={i} style={{ padding: 12, borderRadius: 8, background: 'var(--bg-tertiary)', marginBottom: 8, borderLeft: '3px solid #a855f7' }}>
                <div style={{ fontSize: '0.85rem', fontWeight: 600 }}>{p.split(':')[0]}</div>
                {p.includes(':') && <div style={{ fontSize: '0.78rem', color: 'var(--text-secondary)', marginTop: 2 }}>{p.split(':').slice(1).join(':').trim()}</div>}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Workflows tab */}
      {tab === 'workflows' && workflows && (
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20 }}>
          <div>
            <div style={{ background: 'var(--bg-secondary)', borderRadius: 12, padding: 20, marginBottom: 16 }}>
              <h3 style={{ marginBottom: 12, fontWeight: 700 }}>⚙️ DMCA Automations</h3>
              <p style={{ fontSize: '0.78rem', color: 'var(--text-secondary)', marginBottom: 12 }}>Source: {workflows.source}</p>
              {workflows.dmca_workflows.map((wf, i) => (
                <div key={i} style={{ padding: 14, borderRadius: 8, background: 'var(--bg-tertiary)', marginBottom: 8, borderLeft: '3px solid #f59e0b' }}>
                  <div style={{ fontSize: '0.92rem', fontWeight: 700, marginBottom: 4 }}>{wf.name}</div>
                  <div style={{ fontSize: '0.8rem', color: 'var(--text-primary)', marginBottom: 4 }}>
                    <strong>Steps:</strong> {wf.steps.join(' → ')}
                  </div>
                  <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
                    🛠️ {wf.tools}
                  </div>
                </div>
              ))}
            </div>
          </div>
          <div>
            <div style={{ background: 'var(--bg-secondary)', borderRadius: 12, padding: 20, marginBottom: 16 }}>
              <h3 style={{ marginBottom: 12, fontWeight: 700 }}>💻 Developer Automations</h3>
              {workflows.dev_workflows.map((wf, i) => (
                <div key={i} style={{ padding: '8px 12px', borderRadius: 8, background: 'var(--bg-tertiary)', marginBottom: 6, fontSize: '0.85rem', borderLeft: '3px solid #10b981' }}>
                  ⚙️ {wf}
                </div>
              ))}
            </div>
            <div style={{ background: 'var(--bg-secondary)', borderRadius: 12, padding: 20 }}>
              <h3 style={{ marginBottom: 12, fontWeight: 700 }}>🛠️ Developer Tools</h3>
              {workflows.dev_tools.map((t, i) => (
                <div key={i} style={{ padding: '8px 12px', borderRadius: 8, background: 'var(--bg-tertiary)', marginBottom: 6, fontSize: '0.85rem', borderLeft: '3px solid #3b82f6' }}>
                  🔧 {t}
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
