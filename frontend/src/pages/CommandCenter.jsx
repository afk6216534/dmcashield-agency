import { useState, useEffect } from 'react';

const API = import.meta.env.VITE_API_URL || 'https://dmcashield-agency.vercel.app';

export default function CommandCenter() {
  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API}/api/dashboard`)
      .then(r => r.json())
      .then(d => { setDashboard(d); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  if (loading) return <div className="p-6">Loading...</div>;

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">🎛️ Command Center</h1>
        <span className="bg-green-600 px-3 py-1 rounded text-sm">System Operational</span>
      </div>

      <div className="grid grid-cols-4 gap-4 mb-6">
        <div className="bg-gradient-to-br from-blue-600 to-blue-800 p-6 rounded-xl">
          <p className="text-blue-200 text-sm">Emails Today</p>
          <p className="text-3xl font-bold">{dashboard?.stats?.emails_sent_today}</p>
          <p className="text-blue-300 text-sm mt-2">↑ 12% vs yesterday</p>
        </div>
        <div className="bg-gradient-to-br from-green-600 to-green-800 p-6 rounded-xl">
          <p className="text-green-200 text-sm">Opened Today</p>
          <p className="text-3xl font-bold">{dashboard?.stats?.emails_opened_today}</p>
          <p className="text-green-300 text-sm mt-2">28% open rate</p>
        </div>
        <div className="bg-gradient-to-br from-purple-600 to-purple-800 p-6 rounded-xl">
          <p className="text-purple-200 text-sm">Replies Today</p>
          <p className="text-3xl font-bold">{dashboard?.stats?.replies_today}</p>
          <p className="text-purple-300 text-sm mt-2">7.1% reply rate</p>
        </div>
        <div className="bg-gradient-to-br from-orange-600 to-orange-800 p-6 rounded-xl">
          <p className="text-orange-200 text-sm">Hot Leads</p>
          <p className="text-3xl font-bold">{dashboard?.stats?.hot_leads}</p>
          <p className="text-orange-300 text-sm mt-2">Ready to convert</p>
        </div>
      </div>

      <div className="mb-6">
        <h2 className="text-xl font-bold mb-3">🏢 Departments</h2>
        <div className="grid grid-cols-4 gap-3">
          {Object.entries(dashboard?.departments || {}).map(([name, dept]) => (
            <div key={name} className="bg-gray-800 p-3 rounded-lg">
              <div className="flex justify-between items-center mb-2">
                <span className="font-bold capitalize">{name}</span>
                <span className={`w-2 h-2 rounded-full ${dept.head.status === 'online' ? 'bg-green-500' : 'bg-red-500'}`}></span>
              </div>
              <p className="text-sm text-gray-400">{dept.head.name}</p>
              <p className="text-xs text-blue-400">{dept.team_size} agents • {dept.head.tasks_completed} tasks</p>
            </div>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-2 gap-6">
        <div className="bg-gray-800 p-4 rounded-lg">
          <h2 className="text-lg font-bold mb-3">🚀 Active Tasks</h2>
          <div className="space-y-2">
            {dashboard?.active_tasks?.map(task => (
              <div key={task.id} className="bg-gray-700 p-3 rounded">
                <div className="flex justify-between">
                  <span className="font-bold">{task.business_type} - {task.city}</span>
                  <span className="text-sm text-gray-400">{task.status}</span>
                </div>
                <div className="mt-2 flex gap-4 text-sm">
                  <span>📧 {task.leads_emailed}/{task.leads_total}</span>
                  <span>🔥 {task.leads_hot} hot</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-gray-800 p-4 rounded-lg">
          <h2 className="text-lg font-bold mb-3">💾 System Soul</h2>
          <div className="grid grid-cols-2 gap-3">
            <div className="bg-gray-700 p-3 rounded text-center">
              <p className="text-2xl font-bold">{dashboard?.soul?.total_leads_processed}</p>
              <p className="text-gray-400 text-sm">Total Leads</p>
            </div>
            <div className="bg-gray-700 p-3 rounded text-center">
              <p className="text-2xl font-bold">{dashboard?.soul?.total_emails_sent}</p>
              <p className="text-gray-400 text-sm">Emails Sent</p>
            </div>
            <div className="bg-gray-700 p-3 rounded text-center">
              <p className="text-2xl font-bold">{dashboard?.soul?.total_clients_acquired}</p>
              <p className="text-gray-400 text-sm">Clients</p>
            </div>
            <div className="bg-gray-700 p-3 rounded text-center">
              <p className="text-2xl font-bold">{dashboard?.soul?.learning_cycle}</p>
              <p className="text-gray-400 text-sm">Learning Cycle</p>
            </div>
          </div>
        </div>
      </div>

      <div className="mt-6 bg-gray-800 p-4 rounded-lg">
        <h2 className="text-lg font-bold mb-3">🔔 Recent Activity</h2>
        <div className="space-y-2">
          {dashboard?.recent_activity?.map((activity, i) => (
            <div key={i} className="flex items-center gap-3 text-sm">
              <span className="text-blue-400">{activity.from_agent}</span>
              <span>→</span>
              <span className="text-green-400">{activity.to_agent}</span>
              <span className="text-gray-400">- {activity.notes}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}