import React, { useState } from 'react';

export default function LaunchTask() {
  const [form, setForm] = useState({ business_type: '', city: '', state: '' });
  const [status, setStatus] = useState('idle');

  const handleSubmit = (e) => {
    e.preventDefault();
    setStatus('launching');
    fetch('/api/tasks', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form)
    }).then(() => setStatus('launched'));
  };

  return (
    <div className="launch-page">
      <h1>Launch Campaign</h1>
      <form onSubmit={handleSubmit}>
        <input placeholder="Business Type" onChange={e => setForm({...form, business_type: e.target.value})} />
        <input placeholder="City" onChange={e => setForm({...form, city: e.target.value})} />
        <input placeholder="State" onChange={e => setForm({...form, state: e.target.value})} />
        <button type="submit" disabled={status === 'launching'}>
          {status === 'launching' ? 'Launching...' : 'Launch Campaign'}
        </button>
      </form>
    </div>
  );
}