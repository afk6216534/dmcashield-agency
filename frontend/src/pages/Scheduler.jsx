import { useState, useEffect } from 'react';

const API = import.meta.env.VITE_API_URL || 'https://dmcashield-agency.vercel.app';

export default function Scheduler() {
  const [schedules, setSchedules] = useState([]);
  const [campaigns, setCampaigns] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [newSchedule, setNewSchedule] = useState({ campaign_id: '', scheduled_at: '', action: 'send_batch', leads_count: 20 });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      fetch(`${API}/api/scheduler`).then(r => r.json()),
      fetch(`${API}/api/campaigns`).then(r => r.json())
    ]).then(([s, c]) => {
      setSchedules(s);
      setCampaigns(c);
      setLoading(false);
    }).catch(() => setLoading(false));
  }, []);

  const createSchedule = async () => {
    const res = await fetch(`${API}/api/scheduler`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newSchedule)
    });
    const data = await res.json();
    setSchedules([...schedules, { ...newSchedule, id: data.id, status: 'pending' }]);
    setShowForm(false);
  };

  const getStatusColor = (status) => {
    if (status === 'completed') return '#10b981';
    if (status === 'running') return '#3b82f6';
    if (status === 'pending') return '#f59e0b';
    return '#6b7280';
  };

  if (loading) return <div className="p-6">Loading...</div>;

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">📅 Campaign Scheduler</h1>
        <button onClick={() => setShowForm(!showForm)} className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
          + New Schedule
        </button>
      </div>

      {showForm && (
        <div className="bg-gray-800 p-4 rounded-lg mb-6">
          <div className="grid grid-cols-2 gap-4 mb-4">
            <div>
              <label className="block text-gray-400 mb-2">Campaign</label>
              <select value={newSchedule.campaign_id} onChange={e => setNewSchedule({...newSchedule, campaign_id: e.target.value})}
                className="w-full bg-gray-700 text-white p-2 rounded">
                <option value="">Select campaign...</option>
                {campaigns.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
              </select>
            </div>
            <div>
              <label className="block text-gray-400 mb-2">Date & Time</label>
              <input type="datetime-local" value={newSchedule.scheduled_at}
                onChange={e => setNewSchedule({...newSchedule, scheduled_at: e.target.value})}
                className="w-full bg-gray-700 text-white p-2 rounded" />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4 mb-4">
            <div>
              <label className="block text-gray-400 mb-2">Action</label>
              <select value={newSchedule.action} onChange={e => setNewSchedule({...newSchedule, action: e.target.value})}
                className="w-full bg-gray-700 text-white p-2 rounded">
                <option value="send_batch">Send Batch</option>
                <option value="follow_up">Follow Up</option>
                <option value="warmup">Email Warmup</option>
              </select>
            </div>
            <div>
              <label className="block text-gray-400 mb-2">Leads Count</label>
              <input type="number" value={newSchedule.leads_count} onChange={e => setNewSchedule({...newSchedule, leads_count: parseInt(e.target.value)})}
                className="w-full bg-gray-700 text-white p-2 rounded" />
            </div>
          </div>
          <button onClick={createSchedule} className="bg-green-600 text-white px-4 py-2 rounded">Schedule</button>
        </div>
      )}

      <div className="bg-gray-800 rounded-lg overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-700">
            <tr>
              <th className="p-3 text-left">Campaign</th>
              <th className="p-3 text-left">Scheduled</th>
              <th className="p-3 text-left">Action</th>
              <th className="p-3 text-left">Leads</th>
              <th className="p-3 text-left">Status</th>
            </tr>
          </thead>
          <tbody>
            {schedules.map(sch => {
              const campaign = campaigns.find(c => c.id === sch.campaign_id);
              return (
                <tr key={sch.id} className="border-t border-gray-700 hover:bg-gray-750">
                  <td className="p-3">{campaign?.name || sch.campaign_id}</td>
                  <td className="p-3">{new Date(sch.scheduled_at).toLocaleString()}</td>
                  <td className="p-3">{sch.action}</td>
                  <td className="p-3">{sch.leads_count}</td>
                  <td className="p-3">
                    <span style={{ color: getStatusColor(sch.status), fontWeight: 'bold' }}>{sch.status}</span>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {schedules.length === 0 && (
        <div className="text-center py-12 text-gray-400">
          <p className="text-4xl mb-4">📅</p>
          <p>No scheduled campaigns</p>
        </div>
      )}
    </div>
  );
}