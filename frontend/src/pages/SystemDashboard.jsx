import { useState, useEffect } from 'react';

const API = 'http://localhost:8000';

export default function SystemDashboard() {
  const [status, setStatus] = useState(null);
  const [leads, setLeads] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [campaigns, setCampaigns] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isLocal, setIsLocal] = useState(true);
  const [lastUpdate, setLastUpdate] = useState(null);

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 30000);
    return () => clearInterval(interval);
  }, []);

  const loadData = async () => {
    setLoading(true);
    setLastUpdate(new Date().toLocaleTimeString());
    try {
      setIsLocal(API.includes('localhost'));
      const [s, l, t, c] = await Promise.all([
        fetch(`${API}/api/status`).then(r => r.json()).catch(() => null),
        fetch(`${API}/api/leads`).then(r => r.json()).catch(() => []),
        fetch(`${API}/api/tasks`).then(r => r.json()).catch(() => []),
        fetch(`${API}/api/campaigns`).then(r => r.json()).catch(() => [])
      ]);
      setStatus(s);
      setLeads(l);
      setTasks(t);
      setCampaigns(c);
    } catch (e) {
      console.error(e);
    }
    setLoading(false);
  };

  if (loading && !status) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-center">
          <div className="text-4xl mb-4 animate-spin">⏳</div>
          <div className="text-white text-xl">Loading Control Tower...</div>
        </div>
      </div>
    );
  }

  const isConnected = status && status.system;

  const demoData = {
    system: { status: 'operational', version: '3.0.0' },
    departments: {
      scraping: 'online', validation: 'online', marketing: 'online',
      email_sending: 'online', tracking: 'online', sales: 'online'
    },
    stats: { total_leads: 247, hot_leads: 38, open_rate: 28, reply_rate: 9, tasks_active: 7, campaigns: 4 }
  };

  const display = isConnected ? status : demoData;
  const dept = isConnected ? display?.departments || display?.departments_status || {} : demoData.departments;
  const stats = isConnected ? display?.stats || {} : demoData.stats;

  const deptIcons = {
    scraping: '🕵️', validation: '✅', marketing: '📣',
    email_sending: '📧', tracking: '📊', sales: '💰'
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white p-4 md:p-8">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-8">
        <div>
          <h1 className="text-3xl md:text-4xl font-bold">🏢 DMCAShield Control Tower</h1>
          <p className="text-gray-400 mt-1">Autonomous DMCA Agency Dashboard</p>
        </div>
        <div className="mt-4 md:mt-0 flex items-center gap-4">
          <span className="text-gray-400 text-sm">
            {lastUpdate ? `Updated: ${lastUpdate}` : ''}
          </span>
          <button onClick={loadData} className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg font-bold transition">
            🔄 Refresh
          </button>
        </div>
      </div>

      <div className={`p-4 rounded-lg mb-6 border ${isConnected ? 'bg-green-900/30 border-green-500' : 'bg-yellow-900/30 border-yellow-500'}`}>
        <div className="flex items-center gap-3">
          <span className={`w-3 h-3 rounded-full ${isConnected ? 'bg-green-500 animate-pulse' : 'bg-yellow-500'}`}></span>
          <span className={`font-bold ${isConnected ? 'text-green-400' : 'text-yellow-400'}`}>
            {isConnected ? '✅ LIVE CONNECTED' : '⚠️ DEMO MODE'}
          </span>
        </div>
        <p className="text-gray-400 text-sm mt-1">
          {isConnected
            ? `Backend: ${API} | Showing real-time data`
            : 'Showing demo data | Start backend for live data'}
        </p>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <div className="bg-gray-800 p-4 md:p-6 rounded-xl border border-green-500/50">
          <div className="text-2xl md:text-3xl font-bold text-green-400">{display?.system?.status || 'operational'}</div>
          <div className="text-gray-400 text-sm">System Status</div>
        </div>
        <div className="bg-gray-800 p-4 md:p-6 rounded-xl border border-blue-500/50">
          <div className="text-2xl md:text-3xl font-bold text-blue-400">{stats.total_leads || 0}</div>
          <div className="text-gray-400 text-sm">Total Leads</div>
        </div>
        <div className="bg-gray-800 p-4 md:p-6 rounded-xl border border-red-500/50">
          <div className="text-2xl md:text-3xl font-bold text-red-400">{stats.hot_leads || 0}</div>
          <div className="text-gray-400 text-sm">Hot Leads</div>
        </div>
        <div className="bg-gray-800 p-4 md:p-6 rounded-xl border border-purple-500/50">
          <div className="text-2xl md:text-3xl font-bold text-purple-400">{stats.campaigns || 0}</div>
          <div className="text-gray-400 text-sm">Campaigns</div>
        </div>
      </div>

      <h2 className="text-xl md:text-2xl font-bold mb-4">🏢 Departments</h2>
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3 mb-8">
        {Object.entries(dept).map(([d, s]) => (
          <div key={d} className={`p-4 rounded-xl border text-center transition ${s === 'online' ? 'bg-green-900/20 border-green-500 hover:bg-green-900/30' : 'bg-red-900/20 border-red-500 hover:bg-red-900/30'}`}>
            <div className="text-3xl mb-2">{deptIcons[d] || '📦'}</div>
            <div className="text-sm font-semibold capitalize">{d.replace('_', ' ')}</div>
            <div className={`text-xs mt-1 ${s === 'online' ? 'text-green-400' : 'text-red-400'}`}>
              ● {s}
            </div>
          </div>
        ))}
      </div>

      <div className="grid md:grid-cols-2 gap-6 mb-8">
        <div className="bg-gray-800 p-6 rounded-xl">
          <h3 className="text-lg font-bold mb-4 flex items-center gap-2">📊 Performance</h3>
          <div className="space-y-3">
            <div className="flex justify-between items-center p-2 bg-gray-700/50 rounded">
              <span className="text-gray-400">Open Rate</span>
              <span className="text-green-400 font-bold text-xl">{stats.open_rate || 0}%</span>
            </div>
            <div className="flex justify-between items-center p-2 bg-gray-700/50 rounded">
              <span className="text-gray-400">Reply Rate</span>
              <span className="text-green-400 font-bold text-xl">{stats.reply_rate || 0}%</span>
            </div>
            <div className="flex justify-between items-center p-2 bg-gray-700/50 round ed">
              <span className="text-gray-400">Active Tasks</span>
              <span className="text-blue-400 font-bold text-xl">{stats.tasks_active || 0}</span>
            </div>
          </div>
        </div>

        <div className="bg-gray-800 p-6 rounded-xl">
          <h3 className="text-lg font-bold mb-4 flex items-center gap-2">👥 Leads</h3>
          <div className="space-y-3">
            <div className="flex justify-between items-center p-2 bg-gray-700/50 rounded">
              <span className="text-gray-400">Total Leads</span>
              <span className="text-blue-400 font-bold text-xl">{leads.length || stats.total_leads || 0}</span>
            </div>
            <div className="flex justify-between items-center p-2 bg-gray-700/50 rounded">
              <span className="text-gray-400">Hot Leads</span>
              <span className="text-red-400 font-bold text-xl">{stats.hot_leads || 0}</span>
            </div>
          </div>
        </div>
      </div>

      <h2 className="text-xl font-bold mb-4">📋 Active Tasks</h2>
      <div className="bg-gray-800 rounded-xl overflow-hidden mb-8">
        {tasks.length === 0 && isConnected ? (
          <div className="p-6 text-center text-gray-500">No active tasks</div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-700">
                <tr>
                  <th className="p-4 text-left">Task</th>
                  <th className="p-4 text-left">Status</th>
                  <th className="p-4 text-left">Progress</th>
                </tr>
              </thead>
              <tbody>
                {(tasks.length > 0 ? tasks : [
                  { id: 1, title: 'DMCA Scraper - Finding targets', status: 'running', progress: 73 },
                  { id: 2, title: 'Email Outreach Campaign', status: 'active', progress: 45 },
                  { id: 3, title: 'Lead Validation Pipeline', status: 'active', progress: 89 }
                ]).map(task => (
                  <tr key={task.id} className="border-t border-gray-700">
                    <td className="p-4">{task.title}</td>
                    <td className="p-4">
                      <span className={`px-3 py-1 rounded-full text-sm ${
                        task.status === 'active' || task.status === 'running'
                          ? 'bg-green-900 text-green-400'
                          : 'bg-gray-700'
                      }`}>
                        {task.status}
                      </span>
                    </td>
                    <td className="p-4 w-32">
                      <div className="w-full bg-gray-700 rounded-full h-2">
                        <div
                          className="bg-green-500 h-2 rounded-full transition-all"
                          style={{width: `${task.progress || 0}%`}}
                        ></div>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      <h2 className="text-xl font-bold mb-4">📣 Campaigns</h2>
      <div className="bg-gray-800 rounded-xl overflow-hidden">
        {campaigns.length === 0 && isConnected ? (
          <div className="p-6 text-center text-gray-500">No campaigns</div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-700">
                <tr>
                  <th className="p-4 text-left">Campaign</th>
                  <th className="p-4 text-left">Status</th>
                  <th className="p-4 text-left">Sent</th>
                  <th className="p-4 text-left">Open Rate</th>
                </tr>
              </thead>
              <tbody>
                {(campaigns.length > 0 ? campaigns : [
                  { id: 1, name: 'DMCA Removal Outreach', status: 'active', sent: 1247, opened: 349 },
                  { id: 2, name: 'Review Response Campaign', status: 'running', sent: 892, opened: 234 },
                  { id: 3, name: 'Partner Invitation', status: 'active', sent: 456, opened: 123 }
                ]).map(camp => (
                  <tr key={camp.id} className="border-t border-gray-700">
                    <td className="p-4">{camp.name}</td>
                    <td className="p-4">
                      <span className="px-3 py-1 rounded-full text-sm bg-green-900 text-green-400">
                        {camp.status}
                      </span>
                    </td>
                    <td className="p-4">{camp.sent || 0}</td>
                    <td className="p-4">
                      <span className="text-green-400">
                        {camp.sent > 0 ? Math.round((camp.opened || 0) / camp.sent * 100) : 0}%
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}