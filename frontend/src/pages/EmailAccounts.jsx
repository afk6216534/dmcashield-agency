import React, { useState, useEffect } from 'react';

export default function EmailAccounts() {
  const [accounts, setAccounts] = useState([]);
  const [newEmail, setNewEmail] = useState({ email: '', password: '', display: '', provider: 'resend' });

  useEffect(() => {
    fetch('/api/accounts')
      .then(r => r.json())
      .then(setAccounts);
  }, []);

  const addAccount = (e) => {
    e.preventDefault();
    const payload = {
      email_address: newEmail.email,
      app_password: newEmail.password,
      provider: newEmail.provider,
      display_name: newEmail.display || newEmail.email.split('@')[0]
    };
    fetch('/api/accounts', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    }).then(() => {
      setNewEmail({ email: '', password: '', display: '', provider: 'resend' });
      fetch('/api/accounts').then(r => r.json()).then(setAccounts);
    });
  };

  const getStatusBadge = (acc) => {
    if (acc.status === 'active') return '✅ Connected';
    if (acc.status === 'warming_up') return '🔄 Warming Up';
    if (acc.status === 'error') return '❌ Not Connected';
    return acc.status;
  };

  return (
    <div className="email-accounts" style={{padding: '20px'}}>
      <h1>📧 Email Accounts</h1>
      <p>Add email providers to send outreach emails</p>
      
      <div style={{marginBottom: '20px'}}>
        <label style={{fontWeight: 'bold', marginRight: '10px'}}>Email Provider:</label>
        <select 
          value={newEmail.provider}
          onChange={e => setNewEmail({...newEmail, provider: e.target.value})}
          style={{padding: '8px', borderRadius: '5px', minWidth: '200px'}}
        >
          <option value="resend">🔵 Resend (Recommended - Free 10k/month)</option>
          <option value="gmail">📧 Gmail (Needs App Password)</option>
          <option value="sendgrid">🟣 SendGrid</option>
        </select>
      </div>
      
      <div style={{background: '#f5f5f5', padding: '20px', borderRadius: '10px', marginBottom: '20px'}}>
        <form onSubmit={addAccount}>
          {newEmail.provider === 'resend' ? (
            <>
              <input 
                placeholder="API Key (from resend.com)" 
                value={newEmail.email}
                onChange={e => setNewEmail({...newEmail, email: e.target.value})}
                style={{display: 'block', width: '100%', padding: '10px', marginBottom: '10px'}}
              />
              <input 
                placeholder="Display Name" 
                value={newEmail.display}
                onChange={e => setNewEmail({...newEmail, display: e.target.value})}
                style={{display: 'block', width: '100%', padding: '10px', marginBottom: '10px'}}
              />
            </>
          ) : (
            <>
              <input 
                placeholder="Email Address" 
                value={newEmail.email}
                onChange={e => setNewEmail({...newEmail, email: e.target.value})}
                style={{display: 'block', width: '100%', padding: '10px', marginBottom: '10px'}}
              />
              <input 
                placeholder={newEmail.provider === 'sendgrid' ? "API Key" : "App Password"} 
                type="password" 
                value={newEmail.password}
                onChange={e => setNewEmail({...newEmail, password: e.target.value})}
                style={{display: 'block', width: '100%', padding: '10px', marginBottom: '10px'}}
              />
            </>
          )}
          <button 
            type="submit" 
            style={{
              background: '#4CAF50', 
              color: 'white', 
              padding: '12px 30px', 
              border: 'none', 
              borderRadius: '5px',
              cursor: 'pointer',
              fontSize: '16px'
            }}
          >
            ➕ Add {newEmail.provider === 'resend' ? 'Resend' : 'Email'} Account
          </button>
        </form>
      </div>
      
      <table style={{width: '100%', borderCollapse: 'collapse'}}>
        <thead>
          <tr style={{background: '#333', color: 'white'}}>
            <th style={{padding: '15px', textAlign: 'left'}}>Email</th>
            <th style={{padding: '15px', textAlign: 'left'}}>Status</th>
            <th style={{padding: '15px', textAlign: 'left'}}>Sent Today</th>
            <th style={{padding: '15px', textAlign: 'left'}}>Health</th>
            <th style={{padding: '15px', textAlign: 'left'}}>Actions</th>
          </tr>
        </thead>
        <tbody>
          {accounts.length === 0 ? (
            <tr><td colSpan={5} style={{padding: '20px', textAlign: 'center'}}>No email accounts connected</td></tr>
          ) : accounts.map(acc => (
            <tr key={acc.id} style={{borderBottom: '1px solid #ddd'}}>
              <td style={{padding: '15px'}}>
                <strong>{acc.email_address}</strong><br/>
                <small>{acc.display_name}</small>
              </td>
              <td style={{padding: '15px'}}>
                <span style={{
                  padding: '5px 10px',
                  borderRadius: '5px',
                  background: acc.status === 'active' ? '#4CAF50' : acc.status === 'error' ? '#f44336' : '#ff9800',
                  color: 'white'
                }}>
                  {getStatusBadge(acc)}
                </span>
              </td>
              <td style={{padding: '15px'}}>{acc.sent_today}/{acc.daily_limit}</td>
              <td style={{padding: '15px'}}>{acc.health_score}%</td>
              <td style={{padding: '15px'}}>
                <button style={{background: '#f44336', color: 'white', border: 'none', padding: '5px 10px', borderRadius: '3px', cursor: 'pointer'}}>Remove</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      
      <div style={{marginTop: '30px', background: '#e3f2fd', padding: '20px', borderRadius: '10px'}}>
        <h3>📌 How to get credentials:</h3>
        <ul style={{lineHeight: '2'}}>
          <li><strong>Resend (Recommended):</strong> Go to <a href="https://resend.com" target="_blank">resend.com</a> → Sign up → API Keys → Copy your key</li>
          <li><strong>Gmail:</strong> Need 2FA enabled first, then go to <a href="https://myaccount.google.com/apppasswords" target="_blank">Google App Passwords</a></li>
          <li><strong>SendGrid:</strong> Go to <a href="https://sendgrid.com" target="_blank">sendgrid.com</a> → API Keys</li>
        </ul>
      </div>
    </div>
  );
}