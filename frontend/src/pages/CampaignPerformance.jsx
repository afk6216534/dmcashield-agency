import { useState, useEffect } from 'react';

const API = import.meta.env.VITE_API_URL || 'https://dmcashield-agency.vercel.app';

export default function CampaignPerformance() {
  const [campaigns, setCampaigns] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API}/api/campaigns`)
      .then(r => r.json())
      .then(d => { setCampaigns(d); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  if (loading) return <div className="p-6">Loading...</div>;

  const getStatusColor = (status) => {
    if (status === 'active') return '#10b981';
    if (status === 'paused') return '#f59e0b';
    return '#6b7280';
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">📊 Campaign Performance</h1>

      <div className="grid grid-cols-4 gap-4 mb-6">
        <div className="bg-gradient-to-br from-green-600 to-green-800 p-6 rounded-xl">
          <p className="text-green-200 text-sm">Active Campaigns</p>
          <p className="text-3xl font-bold">{campaigns.filter(c => c.status === 'active').length}</p>
        </div>
        <div className="bg-gradient-to-br from-blue-600 to-blue-800 p-6 rounded-xl">
          <p className="text-blue-200 text-sm">Total Leads</p>
          <p className="text-3xl font-bold">{campaigns.reduce((a, c) => a + c.leads_total, 0)}</p>
        </div>
        <div className="bg-gradient-to-br from-purple-600 to-purple-800 p-6 rounded-xl">
          <p className="text-purple-200 text-sm">Emailed</p>
          <p className="text-3xl font-bold">{campaigns.reduce((a, c) => a + c.leads_emailed, 0)}</p>
        </div>
        <div className="bg-gradient-to-br from-orange-600 to-orange-800 p-6 rounded-xl">
          <p className="text-orange-200 text-sm">Hot Leads</p>
          <p className="text-3xl font-bold">{campaigns.reduce((a, c) => a + c.leads_hot, 0)}</p>
        </div>
      </div>

      <div className="bg-gray-800 rounded-lg overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-700">
            <tr>
              <th className="p-3 text-left">Campaign</th>
              <th className="p-3 text-left">Status</th>
              <th className="p-3 text-left">Leads</th>
              <th className="p-3 text-left">Emailed</th>
              <th className="p-3 text-left">Hot</th>
              <th className="p-3 text-left">Open Rate</th>
              <th className="p-3 text-left">Created</th>
            </tr>
          </thead>
          <tbody>
            {campaigns.map(c => (
              <tr key={c.id} className="border-t border-gray-700 hover:bg-gray-750">
                <td className="p-3 font-bold">{c.name}</td>
                <td className="p-3">
                  <span style={{ color: getStatusColor(c.status), fontWeight: 'bold' }}>{c.status}</span>
                </td>
                <td className="p-3">{c.leads_total}</td>
                <td className="p-3">{c.leads_emailed}</td>
                <td className="p-3">
                  <span className="text-orange-400 font-bold">{c.leads_hot}</span>
                </td>
                <td className="p-3">
                  <div className="flex items-center gap-2">
                    <div className="w-16 bg-gray-700 rounded-full h-2">
                      <div className="bg-blue-500 h-2 rounded-full" style={{ width: `${c.open_rate}%` }}></div>
                    </div>
                    <span>{c.open_rate}%</span>
                  </div>
                </td>
                <td className="p-3 text-gray-400">{new Date(c.created_at).toLocaleDateString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="mt-6 grid grid-cols-2 gap-4">
        <div className="bg-gray-800 p-4 rounded-lg">
          <h2 className="text-lg font-bold mb-3">🔥 Best Performing</h2>
          {campaigns.sort((a, b) => b.leads_hot - a.leads_hot)[0] && (
            <div className="bg-gray-700 p-3 rounded">
              <p className="font-bold">{campaigns.sort((a, b) => b.leads_hot - a.leads_hot)[0].name}</p>
              <p className="text-orange-400">{campaigns.sort((a, b) => b.leads_hot - a.leads_hot)[0].leads_hot} hot leads</p>
            </div>
          )}
        </div>
        <div className="bg-gray-800 p-4 rounded-lg">
          <h2 className="text-lg font-bold mb-3">📈 Highest Open Rate</h2>
          {campaigns.sort((a, b) => b.open_rate - a.open_rate)[0] && (
            <div className="bg-gray-700 p-3 rounded">
              <p className="font-bold">{campaigns.sort((a, b) => b.open_rate - a.open_rate)[0].name}</p>
              <p className="text-blue-400">{campaigns.sort((a, b) => b.open_rate - a.open_rate)[0].open_rate}% open rate</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}