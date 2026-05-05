import { useState, useEffect } from 'react';

const API = import.meta.env.VITE_API_URL || 'https://dmcashield-agency.vercel.app';

export default function EmailDetailed() {
  const [accounts, setAccounts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API}/api/accounts`)
      .then(r => r.json())
      .then(d => { setAccounts(d); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  const addAccount = async () => {
    const email = prompt('Enter email address:');
    if (email) {
      const res = await fetch(`${API}/api/accounts`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email_address: email, display_name: 'New Account' })
      });
      const data = await res.json();
      setAccounts([...accounts, { id: data.id, email_address: email, status: 'warming_up', sent_today: 0 }]);
    }
  };

  const getHealthColor = (score) => {
    if (score >= 90) return '#10b981';
    if (score >= 70) return '#3b82f6';
    return '#f59e0b';
  };

  if (loading) return <div className="p-6">Loading...</div>;

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">📧 Email Account Management</h1>
        <button onClick={addAccount} className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
          + Add Account
        </button>
      </div>

      <div className="grid grid-cols-4 gap-4 mb-6">
        <div className="bg-gradient-to-br from-green-600 to-green-800 p-6 rounded-xl">
          <p className="text-green-200 text-sm">Active</p>
          <p className="text-3xl font-bold">{accounts.filter(a => a.status === 'active').length}</p>
        </div>
        <div className="bg-gradient-to-br from-orange-600 to-orange-800 p-6 rounded-xl">
          <p className="text-orange-200 text-sm">Warming Up</p>
          <p className="text-3xl font-bold">{accounts.filter(a => a.status === 'warming_up').length}</p>
        </div>
        <div className="bg-gradient-to-br from-blue-600 to-blue-800 p-6 rounded-xl">
          <p className="text-blue-200 text-sm">Sent Today</p>
          <p className="text-3xl font-bold">{accounts.reduce((a, c) => a + c.sent_today, 0)}</p>
        </div>
        <div className="bg-gradient-to-br from-purple-600 to-purple-800 p-6 rounded-xl">
          <p className="text-purple-200 text-sm">Total Sent</p>
          <p className="text-3xl font-bold">{accounts.reduce((a, c) => a + c.total_sent, 0)}</p>
        </div>
      </div>

      <div className="grid gap-4">
        {accounts.map(account => (
          <div key={account.id} className="bg-gray-800 p-4 rounded-lg">
            <div className="flex justify-between items-start mb-4">
              <div>
                <h3 className="font-bold text-lg">{account.display_name}</h3>
                <p className="text-gray-400">{account.email_address}</p>
              </div>
              <span className={`px-3 py-1 rounded text-sm ${account.status === 'active' ? 'bg-green-900 text-green-400' : 'bg-orange-900 text-orange-400'}`}>
                {account.status.replace('_', ' ')}
              </span>
            </div>

            <div className="grid grid-cols-4 gap-4 mb-4">
              <div className="bg-gray-700 p-3 rounded text-center">
                <p className="text-gray-400 text-sm">Daily Limit</p>
                <p className="font-bold">{account.daily_limit}</p>
              </div>
              <div className="bg-gray-700 p-3 rounded text-center">
                <p className="text-gray-400 text-sm">Sent Today</p>
                <p className="font-bold">{account.sent_today}</p>
              </div>
              <div className="bg-gray-700 p-3 rounded text-center">
                <p className="text-gray-400 text-sm">Total Sent</p>
                <p className="font-bold">{account.total_sent}</p>
              </div>
              <div className="bg-gray-700 p-3 rounded text-center">
                <p className="text-gray-400 text-sm">Warmup Day</p>
                <p className="font-bold">{account.warmup_day}/28</p>
              </div>
            </div>

            <div className="grid grid-cols-3 gap-4">
              <div className="bg-gray-700 p-3 rounded">
                <p className="text-gray-400 text-sm">Health Score</p>
                <div className="flex items-center gap-2">
                  <div className="flex-1 bg-gray-600 rounded-full h-2">
                    <div style={{ width: `${account.health_score}%`, backgroundColor: getHealthColor(account.health_score) }} className="h-2 rounded-full"></div>
                  </div>
                  <span style={{ color: getHealthColor(account.health_score) }}>{account.health_score}%</span>
                </div>
              </div>
              <div className="bg-gray-700 p-3 rounded">
                <p className="text-gray-400 text-sm">Total Opens</p>
                <p className="font-bold">{account.total_opens}</p>
              </div>
              <div className="bg-gray-700 p-3 rounded">
                <p className="text-gray-400 text-sm">Total Replies</p>
                <p className="font-bold">{account.total_replies}</p>
              </div>
            </div>

            <div className="mt-4 flex gap-2">
              <button className="bg-blue-600 px-3 py-1 rounded text-sm">Configure</button>
              {account.status === 'warming_up' && (
                <button className="bg-green-600 px-3 py-1 rounded text-sm">Start Warmup</button>
              )}
              <button className="bg-red-600 px-3 py-1 rounded text-sm">Remove</button>
            </div>
          </div>
        ))}
      </div>

      {accounts.length === 0 && (
        <div className="text-center py-12 text-gray-400">
          <p className="text-4xl mb-4">📧</p>
          <p>No email accounts yet</p>
          <button onClick={addAccount} className="mt-4 bg-blue-600 px-4 py-2 rounded">Add Account</button>
        </div>
      )}
    </div>
  );
}