import { useState, useEffect } from 'react';

const API = import.meta.env.VITE_API_URL || 'https://dmcashield-agency.vercel.app';

export default function Clients() {
  const [clients, setClients] = useState([]);
  const [revenue, setRevenue] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      fetch(`${API}/api/clients`).then(r => r.json()),
      fetch(`${API}/api/revenue`).then(r => r.json())
    ]).then(([c, rev]) => {
      setClients(c);
      setRevenue(rev);
      setLoading(false);
    }).catch(() => setLoading(false));
  }, []);

  const getPlanColor = (plan) => plan === 'pro' ? '#10b981' : '#6366f1';

  if (loading) return <div className="p-6">Loading...</div>;

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">Client Management</h1>
      
      {revenue && (
        <div className="grid grid-cols-4 gap-4 mb-6">
          <div className="bg-gray-800 p-4 rounded-lg">
            <p className="text-gray-400 text-sm">Monthly Revenue</p>
            <p className="text-2xl font-bold text-green-400">${revenue.monthly_revenue.toLocaleString()}</p>
          </div>
          <div className="bg-gray-800 p-4 rounded-lg">
            <p className="text-gray-400 text-sm">Active Clients</p>
            <p className="text-2xl font-bold">{revenue.active_clients}</p>
          </div>
          <div className="bg-gray-800 p-4 rounded-lg">
            <p className="text-gray-400 text-sm">Avg Client Value</p>
            <p className="text-2xl font-bold">${revenue.avg_client_value}</p>
          </div>
          <div className="bg-gray-800 p-4 rounded-lg">
            <p className="text-gray-400 text-sm">Annual Projection</p>
            <p className="text-2xl font-bold text-blue-400">${revenue.annual_projection.toLocaleString()}</p>
          </div>
        </div>
      )}

      <div className="bg-gray-800 rounded-lg overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-700">
            <tr>
              <th className="p-3 text-left">Business</th>
              <th className="p-3 text-left">Owner</th>
              <th className="p-3 text-left">Plan</th>
              <th className="p-3 text-left">DMCA Cases</th>
              <th className="p-3 text-left">Total Spent</th>
              <th className="p-3 text-left">Status</th>
            </tr>
          </thead>
          <tbody>
            {clients.map(client => (
              <tr key={client.id} className="border-t border-gray-700 hover:bg-gray-750">
                <td className="p-3">{client.business_name}</td>
                <td className="p-3">{client.owner}</td>
                <td className="p-3">
                  <span style={{ color: getPlanColor(client.plan), fontWeight: 'bold' }}>
                    {client.plan.toUpperCase()}
                  </span>
                </td>
                <td className="p-3">{client.dmca_cases}</td>
                <td className="p-3">${client.total_spent.toLocaleString()}</td>
                <td className="p-3">
                  <span className={`px-2 py-1 rounded text-xs ${client.status === 'active' ? 'bg-green-900 text-green-400' : 'bg-red-900 text-red-400'}`}>
                    {client.status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {revenue?.recent_payments && (
        <div className="mt-6">
          <h2 className="text-xl font-bold mb-3">Recent Payments</h2>
          <div className="grid gap-2">
            {revenue.recent_payments.map((p, i) => (
              <div key={i} className="bg-gray-800 p-3 rounded flex justify-between">
                <span>{p.client}</span>
                <span className="text-green-400 font-bold">${p.amount}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}