import { useState, useEffect } from 'react';

const API = import.meta.env.VITE_API_URL || 'https://dmcashield-agency.vercel.app';

export default function WarmupDetailed() {
  const [accounts, setAccounts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API}/api/accounts`)
      .then(r => r.json())
      .then(d => { setAccounts(d); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  const startWarmup = async (id) => {
    await fetch(`${API}/api/accounts/${id}/warmup`, { method: 'POST' });
    setAccounts(accounts.map(a => a.id === id ? { ...a, status: 'warming_up' } : a));
  };

  const stopWarmup = async (id) => {
    await fetch(`${API}/api/accounts/${id}/warmup`, { method: 'DELETE' });
    setAccounts(accounts.map(a => a.id === id ? { ...a, status: 'paused' } : a));
  };

  const getProgress = (day) => Math.min((day / 28) * 100, 100);

  const getDayColor = (day) => {
    if (day >= 21) return '#10b981';
    if (day >= 14) return '#3b82f6';
    if (day >= 7) return '#f59e0b';
    return '#6b7280';
  };

  if (loading) return <div className="p-6">Loading...</div>;

  const warmingAccounts = accounts.filter(a => a.status === 'warming_up');
  const completedAccounts = accounts.filter(a => a.warmup_complete);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">🔥 Email Warmup System</h1>

      <div className="grid grid-cols-4 gap-4 mb-6">
        <div className="bg-gradient-to-br from-orange-600 to-orange-800 p-6 rounded-xl">
          <p className="text-orange-200 text-sm">Warming Up</p>
          <p className="text-3xl font-bold">{warmingAccounts.length}</p>
        </div>
        <div className="bg-gradient-to-br from-green-600 to-green-800 p-6 rounded-xl">
          <p className="text-green-200 text-sm">Completed</p>
          <p className="text-3xl font-bold">{completedAccounts.length}</p>
        </div>
        <div className="bg-gradient-to-br from-blue-600 to-blue-800 p-6 rounded-xl">
          <p className="text-blue-200 text-sm">Total Accounts</p>
          <p className="text-3xl font-bold">{accounts.length}</p>
        </div>
        <div className="bg-gradient-to-br from-purple-600 to-purple-800 p-6 rounded-xl">
          <p className="text-purple-200 text-sm">Avg Health</p>
          <p className="text-3xl font-bold">
            {accounts.length ? Math.round(accounts.reduce((a, c) => a + c.health_score, 0) / accounts.length) : 0}%
          </p>
        </div>
      </div>

      <div className="bg-gray-800 p-4 rounded-lg mb-6">
        <h2 className="text-lg font-bold mb-3">📅 28-Day Warmup Schedule</h2>
        <div className="flex gap-1">
          {Array.from({ length: 28 }, (_, i) => i + 1).map(day => (
            <div key={day} className="flex-1 text-center">
              <div className={`h-8 rounded ${day <= Math.max(...accounts.map(a => a.warmup_day || 0)) ? 'bg-green-500' : 'bg-gray-700'}`}></div>
              <p className="text-xs mt-1">{day}</p>
            </div>
          ))}
        </div>
        <div className="flex justify-between text-sm text-gray-400 mt-2">
          <span>Day 1 (5 emails)</span>
          <span>Day 14 (20 emails)</span>
          <span>Day 28 (40 emails)</span>
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
              <span className={`px-3 py-1 rounded text-sm ${account.warmup_complete ? 'bg-green-900 text-green-400' : account.status === 'warming_up' ? 'bg-orange-900 text-orange-400' : 'bg-gray-700 text-gray-400'}`}>
                {account.warmup_complete ? 'Complete' : account.status}
              </span>
            </div>

            <div className="mb-4">
              <div className="flex justify-between text-sm mb-1">
                <span>Warmup Progress</span>
                <span>Day {account.warmup_day}/28 ({getProgress(account.warmup_day).toFixed(0)}%)</span>
              </div>
              <div className="w-full bg-gray-700 rounded-full h-3">
                <div style={{ width: `${getProgress(account.warmup_day)}%`, backgroundColor: getDayColor(account.warmup_day) }} className="h-3 rounded-full"></div>
              </div>
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
                <p className="text-gray-400 text-sm">Total Opens</p>
                <p className="font-bold">{account.total_opens}</p>
              </div>
              <div className="bg-gray-700 p-3 rounded text-center">
                <p className="text-gray-400 text-sm">Health Score</p>
                <p className="font-bold" style={{ color: getDayColor(account.health_score) }}>{account.health_score}%</p>
              </div>
            </div>

            <div className="flex gap-2">
              {!account.warmup_complete && account.status !== 'warming_up' && (
                <button onClick={() => startWarmup(account.id)} className="bg-green-600 px-3 py-1 rounded text-sm">Start Warmup</button>
              )}
              {account.status === 'warming_up' && (
                <button onClick={() => stopWarmup(account.id)} className="bg-yellow-600 px-3 py-1 rounded text-sm">Pause</button>
              )}
              <button className="bg-blue-600 px-3 py-1 rounded text-sm">View Logs</button>
            </div>
          </div>
        ))}

        {accounts.length === 0 && (
          <div className="text-center py-12 text-gray-400">
            <p className="text-4xl mb-4">🔥</p>
            <p>No accounts to warm up</p>
            <p className="text-sm">Add email accounts first</p>
          </div>
        )}
      </div>

      <div className="mt-6 bg-gray-800 p-4 rounded-lg">
        <h2 className="text-lg font-bold mb-3">💡 Warmup Best Practices</h2>
        <div className="grid grid-cols-2 gap-4 text-sm">
          <div className="bg-gray-700 p-3 rounded">
            <p className="text-green-400 font-bold">Start Slow</p>
            <p className="text-gray-400">Day 1-7: 5-10 emails/day</p>
          </div>
          <div className="bg-gray-700 p-3 rounded">
            <p className="text-blue-400 font-bold">Gradual Increase</p>
            <p className="text-gray-400">Day 8-14: 15-25 emails/day</p>
          </div>
          <div className="bg-gray-700 p-3 rounded">
            <p className="text-purple-400 font-bold">Build Reputation</p>
            <p className="text-gray-400">Day 15-21: 25-35 emails/day</p>
          </div>
          <div className="bg-gray-700 p-3 rounded">
            <p className="text-orange-400 font-bold">Full Speed</p>
            <p className="text-gray-400">Day 22-28: 35-40 emails/day</p>
          </div>
        </div>
      </div>
    </div>
  );
}