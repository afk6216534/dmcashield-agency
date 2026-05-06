import { useState, useEffect } from 'react';

const API = import.meta.env.VITE_API_URL || 'https://dmcashield-agency.vercel.app';

export default function Overview() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API}/api/dashboard`)
      .then(r => r.json())
      .then(d => { setStats(d); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  if (loading) return <div className="p-6">Loading...</div>;

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">📊 DMCAShield Overview</h1>

      <div className="grid grid-cols-4 gap-4 mb-6">
        <div className="bg-gradient-to-br from-blue-600 to-blue-800 p-6 rounded-xl">
          <p className="text-blue-200 text-sm">Leads Today</p>
          <p className="text-3xl font-bold">{stats?.stats?.emails_sent_today || 0}</p>
        </div>
        <div className="bg-gradient-to-br from-green-600 to-green-800 p-6 rounded-xl">
          <p className="text-green-200 text-sm">Opened Today</p>
          <p className="text-3xl font-bold">{stats?.stats?.emails_opened_today || 0}</p>
        </div>
        <div className="bg-gradient-to-br from-orange-600 to-orange-800 p-6 rounded-xl">
          <p className="text-orange-200 text-sm">Hot Leads</p>
          <p className="text-3xl font-bold">{stats?.stats?.hot_leads || 0}</p>
        </div>
        <div className="bg-gradient-to-br from-purple-600 to-purple-800 p-6 rounded-xl">
          <p className="text-purple-200 text-sm">Replies Today</p>
          <p className="text-3xl font-bold">{stats?.stats?.replies_today || 0}</p>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-6 mb-6">
        <div className="bg-gray-800 p-4 rounded-lg">
          <h2 className="text-lg font-bold mb-3">🔔 Recent Activity</h2>
          <div className="space-y-2">
            {stats?.recent_activity?.slice(0, 5).map((activity, i) => (
              <div key={i} className="bg-gray-700 p-2 rounded text-sm">
                <span className="text-blue-400">{activity.from_agent}</span> → 
                <span className="text-green-400"> {activity.to_agent}</span>
                <span className="text-gray-400"> - {activity.notes}</span>
              </div>
            ))}
          </div>
        </div>
        <div className="bg-gray-800 p-4 rounded-lg">
          <h2 className="text-lg font-bold mb-3">📈 All-Time Stats</h2>
          <div className="grid grid-cols-2 gap-3">
            <div className="bg-gray-700 p-3 rounded text-center">
              <p className="text-2xl font-bold">{stats?.soul?.total_leads_processed || 0}</p>
              <p className="text-gray-400 text-sm">Total Leads</p>
            </div>
            <div className="bg-gray-700 p-3 rounded text-center">
              <p className="text-2xl font-bold">{stats?.soul?.total_emails_sent || 0}</p>
              <p className="text-gray-400 text-sm">Emails Sent</p>
            </div>
            <div className="bg-gray-700 p-3 rounded text-center">
              <p className="text-2xl font-bold">{stats?.soul?.total_clients_acquired || 0}</p>
              <p className="text-gray-400 text-sm">Clients</p>
            </div>
            <div className="bg-gray-700 p-3 rounded text-center">
              <p className="text-2xl font-bold">{stats?.soul?.learning_cycle || 0}</p>
              <p className="text-gray-400 text-sm">AI Learning</p>
            </div>
          </div>
        </div>
      </div>

      <div className="bg-gray-800 p-4 rounded-lg">
        <h2 className="text-lg font-bold mb-3">✅ Quick Actions</h2>
        <div className="grid grid-cols-4 gap-3">
          <a href="#/launch" className="bg-blue-600 p-3 rounded text-center hover:bg-blue-700">
            <p className="text-2xl">🚀</p>
            <p className="text-sm">Launch</p>
          </a>
          <a href="#/leads" className="bg-green-600 p-3 rounded text-center hover:bg-green-700">
            <p className="text-2xl">👥</p>
            <p className="text-sm">Leads</p>
          </a>
          <a href="#/hot-leads" className="bg-orange-600 p-3 rounded text-center hover:bg-orange-700">
            <p className="text-2xl">🔥</p>
            <p className="text-sm">Hot Leads</p>
          </a>
          <a href="#/ai-detailed" className="bg-purple-600 p-3 rounded text-center hover:bg-purple-700">
            <p className="text-2xl">🤖</p>
            <p className="text-sm">AI Chat</p>
          </a>
        </div>
      </div>
    </div>
  );
}