import React, { useState, useEffect } from 'react';

export default function Settings() {
  const [config, setConfig] = useState({});
  const [jarvisInput, setJarvisInput] = useState('');

  useEffect(() => {
    fetch('/api/status').then(r => r.json()).then(setConfig);
  }, []);

  const sendJarvis = (cmd) => {
    fetch('/api/jarvis', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ command: cmd })
    }).then(r => r.json()).then(r => alert(r.response));
  };

  return (
    <div className="settings">
      <h1>⚙️ Settings & JARVIS</h1>
      <div className="grid">
        <div className="card jarvis">
          <h2>JARVIS Command</h2>
          <input placeholder="Ask JARVIS..." value={jarvisInput}
                onChange={e => setJarvisInput(e.target.value)}
                onKeyPress={e => e.key === 'Enter' && (sendJarvis(jarvisInput), setJarvisInput(''))} />
          <p className="hint">Try: 'Send report' or 'Optimize system'</p>
        </div>
        <div className="card">
          <h2>System Status</h2>
          <p>Status: {config.system?.status}</p>
          <p>Departments: {config.departments_status && Object.values(config.departments_status).filter(s => s === 'online').length}/12 online</p>
        </div>
        <div className="card">
          <h2>Stats</h2>
          <p>Tasks: {config.stats?.total_tasks || 0}</p>
          <p>Leads: {config.stats?.total_leads || 0}</p>
          <p>Hot: {config.stats?.hot_leads || 0}</p>
        </div>
      </div>
    </div>
  );
}