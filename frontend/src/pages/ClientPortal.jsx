import { useState, useEffect } from 'react';

const API = import.meta.env.VITE_API_URL || 'https://dmcashield-agency.vercel.app';

export default function ClientPortal() {
  const [client, setClient] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API}/api/clients`)
      .then(r => r.json())
      .then(d => { setClient(d[0]); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  if (loading) return <div className="p-6">Loading...</div>;

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">👤 Client Portal</h1>

      <div className="bg-gray-800 p-6 rounded-lg mb-6">
        <div className="flex items-center gap-4 mb-4">
          <div className="w-16 h-16 bg-blue-600 rounded-full flex items-center justify-center text-2xl font-bold">
            {client?.business_name?.charAt(0) || 'C'}
          </div>
          <div>
            <h2 className="text-xl font-bold">{client?.business_name || 'Your Business'}</h2>
            <p className="text-gray-400">{client?.owner || 'Owner'}</p>
          </div>
          <span className="ml-auto bg-green-600 px-4 py-2 rounded text-sm">Pro Plan</span>
        </div>

        <div className="grid grid-cols-4 gap-4 mb-4">
          <div className="bg-gray-700 p-4 rounded text-center">
            <p className="text-2xl font-bold">{client?.dmca_cases || 1}</p>
            <p className="text-gray-400 text-sm">DMCA Cases</p>
          </div>
          <div className="bg-gray-700 p-4 rounded text-center">
            <p className="text-2xl font-bold">{client?.total_spent || 2500}</p>
            <p className="text-gray-400 text-sm">Total Spent</p>
          </div>
          <div className="bg-gray-700 p-4 rounded text-center">
            <p className="text-2xl font-bold">12</p>
            <p className="text-gray-400 text-sm">Reviews Removed</p>
          </div>
          <div className="bg-gray-700 p-4 rounded text-center">
            <p className="text-2xl font-bold text-green-400">Active</p>
            <p className="text-gray-400 text-sm">Status</p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-6">
        <div className="bg-gray-800 p-4 rounded-lg">
          <h3 className="font-bold mb-3">📊 Your Performance</h3>
          <div className="space-y-3">
            <div className="flex justify-between">
              <span>Reviews Removed</span>
              <span className="text-green-400 font-bold">12</span>
            </div>
            <div className="flex justify-between">
              <span>Emails Sent</span>
              <span className="text-blue-400 font-bold">847</span>
            </div>
            <div className="flex justify-between">
              <span>Open Rate</span>
              <span className="text-purple-400 font-bold">34%</span>
            </div>
            <div className="flex justify-between">
              <span>Response Rate</span>
              <span className="text-orange-400 font-bold">8%</span>
            </div>
          </div>
        </div>

        <div className="bg-gray-800 p-4 rounded-lg">
          <h3 className="font-bold mb-3">📧 Recent Activity</h3>
          <div className="space-y-2 text-sm">
            <div className="bg-gray-700 p-2 rounded">
              <p className="text-gray-400">May 4 - Email campaign sent to 45 leads</p>
            </div>
            <div className="bg-gray-700 p-2 rounded">
              <p className="text-gray-400">May 3 - 3 negative reviews removed</p>
            </div>
            <div className="bg-gray-700 p-2 rounded">
              <p className="text-gray-400">May 2 - New hot lead identified</p>
            </div>
          </div>
        </div>
      </div>

      <div className="mt-6 bg-gray-800 p-4 rounded-lg">
        <h3 className="font-bold mb-3">📞 Support</h3>
        <div className="flex gap-4">
          <button className="bg-blue-600 px-4 py-2 rounded">Contact Support</button>
          <button className="bg-gray-700 px-4 py-2 rounded">View Invoice</button>
          <button className="bg-gray-700 px-4 py-2 rounded">Upgrade Plan</button>
        </div>
      </div>
    </div>
  );
}