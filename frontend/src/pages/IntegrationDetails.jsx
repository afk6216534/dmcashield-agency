import { useState, useEffect } from 'react';

const API = import.meta.env.VITE_API_URL || 'https://dmcashield-agency.vercel.app';

export default function IntegrationDetails() {
  const [integrations, setIntegrations] = useState([]);
  const [testing, setTesting] = useState(null);
  const [loading, setLoading] = useState(true);

  const integrationList = [
    { id: 'smtp', name: 'SMTP Email', icon: '📧', description: 'Send emails via SMTP' },
    { id: 'imap', name: 'IMAP Reply', icon: '📬', description: 'Receive and monitor replies' },
    { id: 'google_sheets', name: 'Google Sheets', icon: '📊', description: 'Export leads to spreadsheets' },
    { id: 'openrouter', name: 'OpenRouter AI', icon: '🤖', description: 'AI models for content generation' },
    { id: 'resend', name: 'Resend', icon: '📨', description: 'Email delivery service' },
    { id: 'twilio', name: 'Twilio SMS', icon: '📱', description: 'SMS and WhatsApp messaging' },
    { id: 'webhook', name: 'Webhooks', icon: '🔗', description: 'Connect to external services' },
    { id: 'zapier', name: 'Zapier', icon: '⚡', description: 'Connect 5000+ apps' },
  ];

  const testIntegration = async (id) => {
    setTesting(id);
    try {
      const res = await fetch(`${API}/api/integrations/${id}/test`, { method: 'POST' });
      const data = await res.json();
      setIntegrations(prev => ({ ...prev, [id]: data }));
    } catch (e) {
      setIntegrations(prev => ({ ...prev, [id]: { status: 'error', message: 'Failed to test' } }));
    }
    setTesting(null);
  };

  const getStatusBadge = (status) => {
    if (status === 'ok') return <span className="bg-green-900 text-green-400 px-2 py-1 rounded text-sm">Connected</span>;
    if (status === 'fallback') return <span className="bg-yellow-900 text-yellow-400 px-2 py-1 rounded text-sm">Fallback</span>;
    if (status === 'error') return <span className="bg-red-900 text-red-400 px-2 py-1 rounded text-sm">Error</span>;
    return <span className="bg-gray-700 text-gray-400 px-2 py-1 rounded text-sm">Not Tested</span>;
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">🔌 Integration Hub</h1>

      <div className="grid grid-cols-2 gap-4">
        {integrationList.map(int => (
          <div key={int.id} className="bg-gray-800 p-4 rounded-lg">
            <div className="flex justify-between items-start mb-3">
              <div className="flex items-center gap-3">
                <span className="text-3xl">{int.icon}</span>
                <div>
                  <h3 className="font-bold text-lg">{int.name}</h3>
                  <p className="text-gray-400 text-sm">{int.description}</p>
                </div>
              </div>
              {getStatusBadge(integrations[int.id]?.status)}
            </div>
            
            {integrations[int.id]?.message && (
              <div className="bg-gray-700 p-2 rounded mb-3 text-sm">
                {integrations[int.id].message}
              </div>
            )}

            <button 
              onClick={() => testIntegration(int.id)}
              disabled={testing === int.id}
              className="bg-blue-600 text-white px-3 py-1 rounded text-sm hover:bg-blue-700 disabled:opacity-50"
            >
              {testing === int.id ? 'Testing...' : 'Test Connection'}
            </button>
          </div>
        ))}
      </div>

      <div className="mt-8 bg-gray-800 p-4 rounded-lg">
        <h2 className="text-lg font-bold mb-3">📚 API Documentation</h2>
        <div className="text-gray-400 text-sm space-y-2">
          <p><span className="text-blue-400">GET /api/dmca/cases</span> - List all DMCA cases</p>
          <p><span className="text-blue-400">POST /api/dmca/cases</span> - Create new DMCA case</p>
          <p><span className="text-blue-400">GET /api/clients</span> - List all clients</p>
          <p><span className="text-blue-400">GET /api/revenue</span> - Get revenue analytics</p>
          <p><span className="text-blue-400">GET /api/team</span> - Get team/department status</p>
          <p><span className="text-blue-400">GET /api/webhooks</span> - List webhooks</p>
          <p><span className="text-blue-400">GET /api/scheduler</span> - List scheduled campaigns</p>
        </div>
      </div>
    </div>
  );
}