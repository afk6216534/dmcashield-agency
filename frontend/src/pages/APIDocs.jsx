import { useState } from 'react';

export default function APIDocs() {
  const [section, setSection] = useState('leads');

  const endpoints = {
    leads: [
      { method: 'GET', path: '/api/leads', desc: 'List all leads' },
      { method: 'GET', path: '/api/leads/:id', desc: 'Get single lead' },
      { method: 'GET', path: '/api/leads/scored', desc: 'Leads sorted by score' },
      { method: 'GET', path: '/api/leads/export', desc: 'Export as CSV' },
    ],
    tasks: [
      { method: 'GET', path: '/api/tasks', desc: 'List all tasks' },
      { method: 'POST', path: '/api/tasks', desc: 'Create new task' },
      { method: 'POST', path: '/api/tasks/:id/pause', desc: 'Pause task' },
    ],
    campaigns: [
      { method: 'GET', path: '/api/campaigns', desc: 'List campaigns' },
    ],
    dmca: [
      { method: 'GET', path: '/api/dmca/cases', desc: 'List DMCA cases' },
      { method: 'POST', path: '/api/dmca/cases', desc: 'Create case' },
    ],
    clients: [
      { method: 'GET', path: '/api/clients', desc: 'List clients' },
      { method: 'GET', path: '/api/clients/:id', desc: 'Get client' },
    ],
    revenue: [
      { method: 'GET', path: '/api/revenue', desc: 'Revenue analytics' },
    ],
    team: [
      { method: 'GET', path: '/api/team', desc: 'Team & departments' },
    ]
  };

  const getMethodColor = (method) => {
    if (method === 'GET') return 'bg-blue-900 text-blue-400';
    if (method === 'POST') return 'bg-green-900 text-green-400';
    if (method === 'PUT') return 'bg-yellow-900 text-yellow-400';
    if (method === 'DELETE') return 'bg-red-900 text-red-400';
    return 'bg-gray-700';
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">🔌 API Documentation</h1>

      <div className="grid grid-cols-7 gap-4 mb-6">
        {Object.keys(endpoints).map(key => (
          <button key={key} onClick={() => setSection(key)}
            className={`p-3 rounded text-center capitalize ${section === key ? 'bg-blue-600' : 'bg-gray-800 hover:bg-gray-700'}`}>
            {key}
          </button>
        ))}
      </div>

      <div className="bg-gray-800 rounded-lg overflow-hidden">
        <div className="p-4 border-b border-gray-700">
          <h2 className="font-bold capitalize">{section} Endpoints</h2>
        </div>
        {endpoints[section].map((ep, i) => (
          <div key={i} className="p-4 border-b border-gray-700 hover:bg-gray-750 flex items-center gap-4">
            <span className={`px-2 py-1 rounded text-sm font-mono ${getMethodColor(ep.method)}`}>
              {ep.method}
            </span>
            <code className="flex-1 font-mono text-sm">{ep.path}</code>
            <span className="text-gray-400 text-sm">{ep.desc}</span>
          </div>
        ))}
      </div>

      <div className="mt-6 bg-gray-800 p-4 rounded-lg">
        <h2 className="text-lg font-bold mb-3">📡 Base URL</h2>
        <code className="bg-gray-700 px-4 py-2 rounded text-blue-400">
          https://dmcashield-agency.vercel.app
        </code>
      </div>

      <div className="mt-4 bg-gray-800 p-4 rounded-lg">
        <h2 className="text-lg font-bold mb-3">🔑 Authentication</h2>
        <p className="text-gray-400">Include your API key in headers:</p>
        <pre className="bg-gray-700 p-3 rounded mt-2 text-sm">
{`curl -H "Authorization: Bearer YOUR_API_KEY" \\
  https://dmcashield-agency.vercel.app/api/leads`}
        </pre>
      </div>
    </div>
  );
}