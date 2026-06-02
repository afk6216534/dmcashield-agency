import { useState, useEffect, useRef } from 'react';

const API = 'http://localhost:8000';

const DEPARTMENTS = [
  { key: '', label: '🧠 JARVIS (General)', desc: 'Ask anything about the company' },
  { key: 'marketing', label: '📣 Marketing', desc: 'Funnels, copywriting, subject lines' },
  { key: 'sales', label: '💰 Sales', desc: 'Hot leads, conversions, pipeline' },
  { key: 'scraping', label: '🕵️ Scraping', desc: 'Lead finding, Google Maps, targets' },
  { key: 'sending', label: '📧 Sending', desc: 'SMTP, deliverability, throttling' },
  { key: 'analytics', label: '📊 Analytics', desc: 'Open rates, click rates, reports' },
  { key: 'validation', label: '✅ Validation', desc: 'Email verification, enrichment' },
  { key: 'ml', label: '🤖 ML Engine', desc: 'Self-learning, patterns, optimization' },
  { key: 'accounts', label: '👤 Accounts', desc: 'Email accounts, warmup, health' },
  { key: 'tasks', label: '📌 Tasks', desc: 'Active tasks, queue, progress' },
  { key: 'memory', label: '💾 Memory', desc: 'Agent brain, decisions, soul' },
  { key: 'sheets', label: '📋 Sheets', desc: 'Data sync, exports, backups' },
];

export default function JARVISChat() {
  const [messages, setMessages] = useState([
    { role: 'jarvis', text: '🧠 **JARVIS Online.** I\'m your AI executive assistant. I can answer questions, pull data from any department, and execute commands.\n\nTry asking:\n• "status" — Full system overview\n• "marketing funnel" — See the email sequence\n• "hot leads" — Current hot lead count\n• Select a department on the left to chat directly with its head agent.', time: new Date().toLocaleTimeString() }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [selectedDept, setSelectedDept] = useState('');
  const chatRef = useRef(null);

  useEffect(() => {
    if (chatRef.current) chatRef.current.scrollTop = chatRef.current.scrollHeight;
  }, [messages]);

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;
    const msg = input;
    setInput('');
    setMessages(m => [...m, { role: 'user', text: msg, time: new Date().toLocaleTimeString(), dept: selectedDept }]);
    setLoading(true);
    try {
      const endpoint = selectedDept ? `${API}/api/departments/${selectedDept}/chat` : `${API}/api/jarvis/chat`;
      const body = selectedDept ? { message: msg } : { message: msg, department: selectedDept };
      const r = await fetch(endpoint, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      });
      const data = await r.json();
      const responseText = data.response || data.message || 'No response received.';
      setMessages(m => [...m, {
        role: 'jarvis', text: responseText,
        agent: data.agent || 'JARVIS',
        time: new Date().toLocaleTimeString(),
        context: data.context
      }]);
    } catch {
      setMessages(m => [...m, { role: 'jarvis', text: '⚡ Connection issue — make sure the backend is running on localhost:8000', time: new Date().toLocaleTimeString() }]);
    }
    setLoading(false);
  };

  const quickAction = (text) => {
    setInput(text);
  };

  return (
    <main className="main-content" style={{ display: 'flex', gap: '1.5rem', height: 'calc(100vh - 60px)', padding: '1rem' }}>
      {/* Department Selector Sidebar */}
      <div style={{ width: '240px', flexShrink: 0, display: 'flex', flexDirection: 'column', gap: '0.5rem', overflowY: 'auto' }}>
        <h3 style={{ margin: '0 0 0.5rem', fontSize: '0.9rem', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '1px' }}>Talk To</h3>
        {DEPARTMENTS.map(d => (
          <div key={d.key} onClick={() => { setSelectedDept(d.key); setMessages(m => [...m, {
            role: 'jarvis', text: d.key ? `Connected to **${d.label}**. You're now chatting with the ${d.label.split(' ')[1]} department head. Ask anything!` : 'Switched back to **JARVIS General**. I can help with anything across all departments.',
            time: new Date().toLocaleTimeString()
          }]); }}
            style={{
              padding: '0.75rem', borderRadius: '10px', cursor: 'pointer',
              background: selectedDept === d.key ? 'rgba(139, 92, 246, 0.2)' : 'rgba(255,255,255,0.03)',
              border: selectedDept === d.key ? '1px solid var(--primary)' : '1px solid transparent',
              transition: 'all 0.2s'
            }}>
            <div style={{ fontWeight: 600, fontSize: '0.9rem' }}>{d.label}</div>
            <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', marginTop: '0.15rem' }}>{d.desc}</div>
          </div>
        ))}
      </div>

      {/* Chat Area */}
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', minWidth: 0 }}>
        {/* Header */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem', flexShrink: 0 }}>
          <div>
            <h1 style={{ margin: 0, fontSize: '1.5rem' }}>
              {selectedDept ? DEPARTMENTS.find(d => d.key === selectedDept)?.label : '🧠 JARVIS AI Assistant'}
            </h1>
            <p className="text-secondary" style={{ margin: '0.2rem 0 0', fontSize: '0.85rem' }}>
              {selectedDept ? 'Chatting with department head — ask questions or give instructions' : 'Your executive AI assistant — knows everything about the company'}
            </p>
          </div>
          <div style={{ display: 'flex', gap: '0.5rem' }}>
            <button className="btn" onClick={() => setMessages([messages[0]])} style={{ fontSize: '0.8rem' }}>🗑 Clear</button>
          </div>
        </div>

        {/* Messages */}
        <div ref={chatRef} style={{
          flex: 1, overflowY: 'auto', padding: '1rem',
          background: 'rgba(0,0,0,0.2)', borderRadius: '16px', marginBottom: '1rem',
          display: 'flex', flexDirection: 'column', gap: '1rem'
        }}>
          {messages.map((m, i) => (
            <div key={i} style={{ display: 'flex', justifyContent: m.role === 'user' ? 'flex-end' : 'flex-start' }}>
              <div style={{
                maxWidth: '75%', padding: '1rem 1.25rem', borderRadius: m.role === 'user' ? '16px 16px 4px 16px' : '16px 16px 16px 4px',
                background: m.role === 'user' ? 'var(--primary)' : 'rgba(255,255,255,0.06)',
                boxShadow: m.role === 'user' ? '0 2px 8px rgba(139,92,246,0.3)' : 'none'
              }}>
                {m.agent && m.agent !== 'JARVIS' && (
                  <div style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--warning)', marginBottom: '0.3rem' }}>
                    👤 {m.agent}
                  </div>
                )}
                <div style={{ whiteSpace: 'pre-wrap', lineHeight: 1.5, fontSize: '0.9rem' }}>{m.text}</div>
                <div style={{ fontSize: '0.7rem', color: 'rgba(255,255,255,0.4)', marginTop: '0.4rem', textAlign: m.role === 'user' ? 'right' : 'left' }}>{m.time}</div>
              </div>
            </div>
          ))}
          {loading && (
            <div style={{ display: 'flex', gap: '0.3rem', padding: '0.5rem' }}>
              <span style={{ width: 8, height: 8, borderRadius: '50%', background: 'var(--primary)', animation: 'pulse 1s infinite' }}></span>
              <span style={{ width: 8, height: 8, borderRadius: '50%', background: 'var(--primary)', animation: 'pulse 1s infinite 0.2s' }}></span>
              <span style={{ width: 8, height: 8, borderRadius: '50%', background: 'var(--primary)', animation: 'pulse 1s infinite 0.4s' }}></span>
            </div>
          )}
        </div>

        {/* Quick Actions */}
        <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '0.75rem', flexWrap: 'wrap', flexShrink: 0 }}>
          {['status', 'hot leads', 'marketing funnel', 'departments', 'help'].map(q => (
            <button key={q} onClick={() => quickAction(q)} className="btn" style={{ fontSize: '0.8rem', padding: '0.4rem 0.8rem' }}>
              {q}
            </button>
          ))}
        </div>

        {/* Input */}
        <form onSubmit={sendMessage} style={{ display: 'flex', gap: '0.75rem', flexShrink: 0 }}>
          <input value={input} onChange={e => setInput(e.target.value)}
            placeholder={selectedDept ? `Talk to ${DEPARTMENTS.find(d => d.key === selectedDept)?.label}...` : 'Ask JARVIS anything...'}
            disabled={loading}
            style={{
              flex: 1, padding: '1rem 1.25rem', borderRadius: '14px',
              background: 'rgba(255,255,255,0.06)', border: '1px solid rgba(255,255,255,0.1)',
              color: 'var(--text-primary)', fontSize: '0.95rem', outline: 'none',
              transition: 'border-color 0.2s'
            }}
            onFocus={e => e.target.style.borderColor = 'var(--primary)'}
            onBlur={e => e.target.style.borderColor = 'rgba(255,255,255,0.1)'}
          />
          <button className="btn btn-primary" type="submit" disabled={loading}
            style={{ padding: '1rem 1.5rem', borderRadius: '14px', fontSize: '1rem' }}>
            {loading ? '⏳' : '⚡ Send'}
          </button>
        </form>
      </div>
    </main>
  );
}
