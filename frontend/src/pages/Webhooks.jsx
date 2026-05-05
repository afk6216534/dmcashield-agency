import { useState, useEffect } from 'react';

const API = import.meta.env.VITE_API_URL || 'https://dmcashield-agency.vercel.app';

export default function Webhooks() {
  const [webhooks, setWebhooks] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [newWebhook, setNewWebhook] = useState({ url: '', events: [] });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API}/api/webhooks`)
      .then(r => r.json())
      .then(d => { setWebhooks(d); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  const createWebhook = async () => {
    const res = await fetch(`${API}/api/webhooks`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newWebhook)
    });
    const data = await res.json();
    setWebhooks([...webhooks, { ...newWebhook, id: data.id, active: true, created_at: new Date().toISOString() }]);
    setShowForm(false);
    setNewWebhook({ url: '', events: [] });
  };

  const eventOptions = ['lead.created', 'lead.hot', 'lead.replied', 'email.sent', 'email.opened', 'dmca.completed'];

  const toggleEvent = (event) => {
    const events = newWebhook.events.includes(event)
      ? newWebhook.events.filter(e => e !== event)
      : [...newWebhook.events, event];
    setNewWebhook({ ...newWebhook, events });
  };

  if (loading) return <div className="p-6">Loading...</div>;

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">🔗 Webhooks</h1>
        <button onClick={() => setShowForm(!showForm)} className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
          + New Webhook
        </button>
      </div>

      {showForm && (
        <div className="bg-gray-800 p-4 rounded-lg mb-6">
          <div className="mb-4">
            <label className="block text-gray-400 mb-2">Webhook URL</label>
            <input placeholder="https://your-server.com/webhook" value={newWebhook.url} 
              onChange={e => setNewWebhook({...newWebhook, url: e.target.value})}
              className="w-full bg-gray-700 text-white p-2 rounded" />
          </div>
          <div className="mb-4">
            <label className="block text-gray-400 mb-2">Events</label>
            <div className="flex flex-wrap gap-2">
              {eventOptions.map(event => (
                <button key={event} onClick={() => toggleEvent(event)}
                  className={`px-3 py-1 rounded text-sm ${newWebhook.events.includes(event) ? 'bg-blue-600 text-white' : 'bg-gray-700 text-gray-300'}`}>
                  {event}
                </button>
              ))}
            </div>
          </div>
          <button onClick={createWebhook} className="bg-green-600 text-white px-4 py-2 rounded">Create Webhook</button>
        </div>
      )}

      <div className="grid gap-4">
        {webhooks.map(wh => (
          <div key={wh.id} className="bg-gray-800 p-4 rounded-lg">
            <div className="flex justify-between items-start">
              <div>
                <p className="font-mono text-sm text-blue-400">{wh.url}</p>
                <div className="flex gap-2 mt-2">
                  {wh.events?.map((e, i) => (
                    <span key={i} className="bg-gray-700 px-2 py-1 rounded text-xs">{e}</span>
                  ))}
                </div>
              </div>
              <span className={`px-3 py-1 rounded text-sm ${wh.active ? 'bg-green-900 text-green-400' : 'bg-red-900 text-red-400'}`}>
                {wh.active ? 'Active' : 'Inactive'}
              </span>
            </div>
            <p className="text-gray-500 text-sm mt-2">Created: {new Date(wh.created_at).toLocaleDateString()}</p>
          </div>
        ))}
      </div>

      {webhooks.length === 0 && (
        <div className="text-center py-12 text-gray-400">
          <p className="text-4xl mb-4">🔗</p>
          <p>No webhooks configured</p>
          <p className="text-sm">Create a webhook to get real-time updates</p>
        </div>
      )}
    </div>
  );
}