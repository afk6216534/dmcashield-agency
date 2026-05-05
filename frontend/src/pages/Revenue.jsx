import { useState, useEffect } from 'react';

const API = import.meta.env.VITE_API_URL || 'https://dmcashield-agency.vercel.app';

export default function Revenue() {
  const [revenue, setRevenue] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API}/api/revenue`)
      .then(r => r.json())
      .then(d => { setRevenue(d); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  if (loading) return <div className="p-6">Loading...</div>;

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">💰 Revenue Analytics</h1>

      <div className="grid grid-cols-4 gap-4 mb-6">
        <div className="bg-gradient-to-br from-green-600 to-green-800 p-6 rounded-xl">
          <p className="text-green-200 text-sm">Monthly Revenue</p>
          <p className="text-3xl font-bold">${revenue?.monthly_revenue?.toLocaleString()}</p>
          <p className="text-green-300 text-sm mt-2">↑ 12% from last month</p>
        </div>
        <div className="bg-gradient-to-br from-blue-600 to-blue-800 p-6 rounded-xl">
          <p className="text-blue-200 text-sm">Annual Projection</p>
          <p className="text-3xl font-bold">${revenue?.annual_projection?.toLocaleString()}</p>
          <p className="text-blue-300 text-sm mt-2">Based on current</p>
        </div>
        <div className="bg-gradient-to-br from-purple-600 to-purple-800 p-6 rounded-xl">
          <p className="text-purple-200 text-sm">Active Clients</p>
          <p className="text-3xl font-bold">{revenue?.active_clients}</p>
          <p className="text-purple-300 text-sm mt-2">2 new this month</p>
        </div>
        <div className="bg-gradient-to-br from-orange-600 to-orange-800 p-6 rounded-xl">
          <p className="text-orange-200 text-sm">Avg Client Value</p>
          <p className="text-3xl font-bold">${revenue?.avg_client_value}</p>
          <p className="text-orange-300 text-sm mt-2">LTV: 18 months</p>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-6">
        <div className="bg-gray-800 p-4 rounded-lg">
          <h2 className="text-lg font-bold mb-4">Revenue by Plan</h2>
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <span className="text-green-400 font-bold">Pro Plan</span>
              <span className="text-xl">${revenue?.revenue_by_plan?.pro?.toLocaleString()}</span>
            </div>
            <div className="w-full bg-gray-700 rounded-full h-3">
              <div className="bg-green-500 h-3 rounded-full" style={{ width: '68%' }}></div>
            </div>
            <div className="flex justify-between items-center mt-4">
              <span className="text-indigo-400 font-bold">Basic Plan</span>
              <span className="text-xl">${revenue?.revenue_by_plan?.basic?.toLocaleString()}</span>
            </div>
            <div className="w-full bg-gray-700 rounded-full h-3">
              <div className="bg-indigo-500 h-3 rounded-full" style={{ width: '32%' }}></div>
            </div>
          </div>
        </div>

        <div className="bg-gray-800 p-4 rounded-lg">
          <h2 className="text-lg font-bold mb-4">Recent Payments</h2>
          <div className="space-y-2">
            {revenue?.recent_payments?.map((p, i) => (
              <div key={i} className="flex justify-between items-center bg-gray-700 p-3 rounded">
                <div>
                  <p className="font-bold">{p.client}</p>
                  <p className="text-gray-400 text-sm">{new Date(p.date).toLocaleDateString()}</p>
                </div>
                <span className="text-green-400 font-bold text-xl">+${p.amount}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="mt-6 bg-gray-800 p-4 rounded-lg">
        <h2 className="text-lg font-bold mb-3">📈 Growth Metrics</h2>
        <div className="grid grid-cols-3 gap-4">
          <div className="text-center p-4 bg-gray-700 rounded">
            <p className="text-gray-400">MRR Growth</p>
            <p className="text-2xl font-bold text-green-400">+12%</p>
          </div>
          <div className="text-center p-4 bg-gray-700 rounded">
            <p className="text-gray-400">Churn Rate</p>
            <p className="text-2xl font-bold text-yellow-400">2.1%</p>
          </div>
          <div className="text-center p-4 bg-gray-700 rounded">
            <p className="text-gray-400">LTV</p>
            <p className="text-2xl font-bold text-blue-400">$4,788</p>
          </div>
        </div>
      </div>
    </div>
  );
}