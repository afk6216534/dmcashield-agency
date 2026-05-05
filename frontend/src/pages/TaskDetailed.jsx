import { useState, useEffect } from 'react';

const API = import.meta.env.VITE_API_URL || 'https://dmcashield-agency.vercel.app';

export default function TaskDetailed() {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API}/api/tasks`)
      .then(r => r.json())
      .then(d => { setTasks(d); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  const createTask = async () => {
    const business = prompt('Business type (e.g., dentist, clinic):');
    const city = prompt('City:');
    const state = prompt('State (e.g., CA):');
    if (business && city && state) {
      const res = await fetch(`${API}/api/tasks`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ business_type: business, city, state })
      });
      const data = await res.json();
      setTasks([...tasks, { id: data.task_id, business_type: business, city, state, status: 'active' }]);
    }
  };

  const pauseTask = async (id) => {
    await fetch(`${API}/api/tasks/${id}/pause`, { method: 'POST' });
    setTasks(tasks.map(t => t.id === id ? { ...t, status: 'paused' } : t));
  };

  const getPhaseColor = (phase) => {
    if (phase === 'complete') return '#10b981';
    if (phase === 'in_progress') return '#3b82f6';
    return '#6b7280';
  };

  if (loading) return <div className="p-6">Loading...</div>;

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">📋 Task Management</h1>
        <button onClick={createTask} className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
          + New Task
        </button>
      </div>

      <div className="grid grid-cols-4 gap-4 mb-6">
        <div className="bg-gray-800 p-4 rounded-lg text-center">
          <p className="text-gray-400 text-sm">Total Tasks</p>
          <p className="text-2xl font-bold">{tasks.length}</p>
        </div>
        <div className="bg-gray-800 p-4 rounded-lg text-center">
          <p className="text-gray-400 text-sm">Active</p>
          <p className="text-2xl font-bold text-green-400">{tasks.filter(t => t.status === 'active').length}</p>
        </div>
        <div className="bg-gray-800 p-4 rounded-lg text-center">
          <p className="text-gray-400 text-sm">Paused</p>
          <p className="text-2xl font-bold text-yellow-400">{tasks.filter(t => t.status === 'paused').length}</p>
        </div>
        <div className="bg-gray-800 p-4 rounded-lg text-center">
          <p className="text-gray-400 text-sm">Hot Leads</p>
          <p className="text-2xl font-bold text-red-400">{tasks.reduce((a, t) => a + (t.leads_hot || 0), 0)}</p>
        </div>
      </div>

      <div className="grid gap-4">
        {tasks.map(task => (
          <div key={task.id} className="bg-gray-800 p-4 rounded-lg">
            <div className="flex justify-between items-start mb-4">
              <div>
                <h3 className="font-bold text-lg capitalize">{task.business_type} - {task.city}, {task.state}</h3>
                <p className="text-gray-400 text-sm">Created: {task.created_at ? new Date(task.created_at).toLocaleDateString() : 'N/A'}</p>
              </div>
              <div className="flex items-center gap-2">
                <span className={`px-3 py-1 rounded text-sm ${task.status === 'active' ? 'bg-green-900 text-green-400' : 'bg-yellow-900 text-yellow-400'}`}>
                  {task.status}
                </span>
                {task.status === 'active' && (
                  <button onClick={() => pauseTask(task.id)} className="bg-yellow-600 px-2 py-1 rounded text-sm">Pause</button>
                )}
              </div>
            </div>

            <div className="grid grid-cols-5 gap-4 mb-4">
              <div className="bg-gray-700 p-3 rounded text-center">
                <p className="text-gray-400 text-sm">Total Leads</p>
                <p className="font-bold text-xl">{task.leads_total || 0}</p>
              </div>
              <div className="bg-gray-700 p-3 rounded text-center">
                <p className="text-gray-400 text-sm">Emailed</p>
                <p className="font-bold text-xl">{task.leads_emailed || 0}</p>
              </div>
              <div className="bg-gray-700 p-3 rounded text-center">
                <p className="text-gray-400 text-sm">Opened</p>
                <p className="font-bold text-xl">{task.leads_opened || 0}</p>
              </div>
              <div className="bg-gray-700 p-3 rounded text-center">
                <p className="text-gray-400 text-sm">Replied</p>
                <p className="font-bold text-xl">{task.leads_replied || 0}</p>
              </div>
              <div className="bg-gray-700 p-3 rounded text-center">
                <p className="text-gray-400 text-sm">Hot</p>
                <p className="font-bold text-xl text-red-400">{task.leads_hot || 0}</p>
              </div>
            </div>

            <div className="flex gap-2">
              <div className="flex-1 bg-gray-700 p-2 rounded">
                <p className="text-gray-400 text-xs mb-1">Scraping</p>
                <div className="w-full bg-gray-600 rounded-full h-2">
                  <div style={{ width: task.phase_scraping === 'complete' ? '100%' : task.phase_scraping === 'in_progress' ? '50%' : '0%', 
                    backgroundColor: getPhaseColor(task.phase_scraping) }} className="h-2 rounded-full"></div>
                </div>
              </div>
              <div className="flex-1 bg-gray-700 p-2 rounded">
                <p className="text-gray-400 text-xs mb-1">Email</p>
                <div className="w-full bg-gray-600 rounded-full h-2">
                  <div style={{ width: task.phase_email_sending === 'complete' ? '100%' : task.phase_email_sending === 'in_progress' ? '50%' : '0%', 
                    backgroundColor: getPhaseColor(task.phase_email_sending) }} className="h-2 rounded-full"></div>
                </div>
              </div>
              <div className="flex-1 bg-gray-700 p-2 rounded">
                <p className="text-gray-400 text-xs mb-1">Sales</p>
                <div className="w-full bg-gray-600 rounded-full h-2">
                  <div style={{ width: task.phase_sales === 'complete' ? '100%' : task.phase_sales === 'active' ? '30%' : '0%', 
                    backgroundColor: getPhaseColor(task.phase_sales) }} className="h-2 rounded-full"></div>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {tasks.length === 0 && (
        <div className="text-center py-12 text-gray-400">
          <p className="text-4xl mb-4">📋</p>
          <p>No tasks yet</p>
          <button onClick={createTask} className="mt-4 bg-blue-600 px-4 py-2 rounded">Create Task</button>
        </div>
      )}
    </div>
  );
}