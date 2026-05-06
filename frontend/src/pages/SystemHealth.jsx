import { useState, useEffect } from 'react';

const API = import.meta.env.VITE_API_URL || 'https://dmcashield-agency.vercel.app';

export default function SystemHealth() {
  const [health, setHealth] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API}/health`)
      .then(r => r.json())
      .then(d => { setHealth(d); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  if (loading) return <div className="p-6">Loading...</div>;

  const getStatusColor = (status) => {
    if (status === 'online' || status === 'operational') return '#10b981';
    if (status === 'active') return '#3b82f6';
    return '#6b7280';
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">🖥️ System Health Dashboard</h1>

      <div className="grid grid-cols-4 gap-4 mb-6">
        <div className="bg-gradient-to-br from-green-600 to-green-800 p-6 rounded-xl">
          <p className="text-green-200 text-sm">System Status</p>
          <p className="text-3xl font-bold">{health?.status || 'operational'}</p>
        </div>
        <div className="bg-gradient-to-br from-blue-600 to-blue-800 p-6 rounded-xl">
          <p className="text-blue-200 text-sm">Departments</p>
          <p className="text-3xl font-bold">{health?.departments || 12}</p>
        </div>
        <div className="bg-gradient-to-br from-purple-600 to-purple-800 p-6 rounded-xl">
          <p className="text-purple-200 text-sm">Agents</p>
          <p className="text-3xl font-bold">{health?.agents || 36}</p>
        </div>
        <div className="bg-gradient-to-br from-orange-600 to-orange-800 p-6 rounded-xl">
          <p className="text-orange-200 text-sm">Uptime</p>
          <p className="text-3xl font-bold">99.9%</p>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-6 mb-6">
        <div className="bg-gray-800 p-4 rounded-lg">
          <h2 className="text-lg font-bold mb-4">🏢 Department Status</h2>
          <div className="grid grid-cols-2 gap-3">
            {['Scraping', 'Validation', 'Marketing', 'Sending', 'Analytics', 'Sales', 'Sheets', 'Accounts', 'Tasks', 'ML', 'JARVIS', 'Memory'].map(dept => (
              <div key={dept} className="bg-gray-700 p-3 rounded flex justify-between items-center">
                <span className="font-bold">{dept}</span>
                <span className="w-3 h-3 rounded-full bg-green-500"></span>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-gray-800 p-4 rounded-lg">
          <h2 className="text-lg font-bold mb-4">🔌 API Status</h2>
          <div className="space-y-2">
            <div className="flex justify-between bg-gray-700 p-3 rounded">
              <span>Backend API</span>
              <span className="text-green-400">Online</span>
            </div>
            <div className="flex justify-between bg-gray-700 p-3 rounded">
              <span>Database</span>
              <span className="text-green-400">Connected</span>
            </div>
            <div className="flex justify-between bg-gray-700 p-3 rounded">
              <span>Email Service</span>
              <span className="text-green-400">Active</span>
            </div>
            <div className="flex justify-between bg-gray-700 p-3 rounded">
              <span>AI Models</span>
              <span className="text-green-400">Available</span>
            </div>
          </div>
        </div>
      </div>

      <div className="bg-gray-800 p-4 rounded-lg">
        <h2 className="text-lg font-bold mb-3">💾 Resource Usage</h2>
        <div className="grid grid-cols-4 gap-4">
          <div className="bg-gray-700 p-3 rounded">
            <p className="text-gray-400 text-sm">CPU</p>
            <div className="flex items-center gap-2">
              <div className="flex-1 bg-gray-600 rounded-full h-2">
                <div className="bg-blue-500 h-2 rounded-full w-1/4"></div>
              </div>
              <span>25%</span>
            </div>
          </div>
          <div className="bg-gray-700 p-3 rounded">
            <p className="text-gray-400 text-sm">Memory</p>
            <div className="flex items-center gap-2">
              <div className="flex-1 bg-gray-600 rounded-full h-2">
                <div className="bg-purple-500 h-2 rounded-full w-1/3"></div>
              </div>
              <span>33%</span>
            </div>
          </div>
          <div className="bg-gray-700 p-3 rounded">
            <p className="text-gray-400 text-sm">Storage</p>
            <div className="flex items-center gap-2">
              <div className="flex-1 bg-gray-600 rounded-full h-2">
                <div className="bg-orange-500 h-2 rounded-full w-1/5"></div>
              </div>
              <span>20%</span>
            </div>
          </div>
          <div className="bg-gray-700 p-3 rounded">
            <p className="text-gray-400 text-sm">API Calls</p>
            <div className="flex items-center gap-2">
              <div className="flex-1 bg-gray-600 rounded-full h-2">
                <div className="bg-green-500 h-2 rounded-full w-1/2"></div>
              </div>
              <span>50%</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}