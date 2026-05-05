import { useState } from 'react';

export default function LinkedInDetailed() {
  const [campaigns, setCampaigns] = useState([
    { id: 1, name: 'Dentist Outreach', sent: 45, opens: 32, replies: 8, status: 'active' },
    { id: 2, name: 'Law Firm Connect', sent: 28, opens: 18, replies: 3, status: 'paused' },
  ]);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">💼 LinkedIn Outreach</h1>

      <div className="grid grid-cols-4 gap-4 mb-6">
        <div className="bg-gradient-to-br from-blue-600 to-blue-800 p-6 rounded-xl">
          <p className="text-blue-200 text-sm">Messages Sent</p>
          <p className="text-3xl font-bold">{campaigns.reduce((a, c) => a + c.sent, 0)}</p>
        </div>
        <div className="bg-gradient-to-br from-green-600 to-green-800 p-6 rounded-xl">
          <p className="text-green-200 text-sm">Profile Views</p>
          <p className="text-3xl font-bold">67</p>
        </div>
        <div className="bg-gradient-to-br from-purple-600 to-purple-800 p-6 rounded-xl">
          <p className="text-purple-200 text-sm">Connections</p>
          <p className="text-3xl font-bold">23</p>
        </div>
        <div className="bg-gradient-to-br from-orange-600 to-orange-800 p-6 rounded-xl">
          <p className="text-orange-200 text-sm">Replies</p>
          <p className="text-3xl font-bold">{campaigns.reduce((a, c) => a + c.replies, 0)}</p>
        </div>
      </div>

      <div className="bg-gray-800 p-4 rounded-lg mb-6">
        <h2 className="text-lg font-bold mb-4">📋 Active Campaigns</h2>
        <div className="space-y-3">
          {campaigns.map(c => (
            <div key={c.id} className="bg-gray-700 p-4 rounded flex justify-between items-center">
              <div>
                <h3 className="font-bold">{c.name}</h3>
                <p className="text-gray-400 text-sm">{c.sent} sent • {c.opens} views • {c.replies} replies</p>
              </div>
              <span className={`px-3 py-1 rounded ${c.status === 'active' ? 'bg-green-900 text-green-400' : 'bg-gray-600'}`}>
                {c.status}
              </span>
            </div>
          ))}
        </div>
        <button className="mt-4 bg-blue-600 px-4 py-2 rounded text-sm">+ New Campaign</button>
      </div>

      <div className="grid grid-cols-2 gap-6">
        <div className="bg-gray-800 p-4 rounded-lg">
          <h2 className="text-lg font-bold mb-3">🎯 Outreach Templates</h2>
          <div className="space-y-2">
            <div className="bg-gray-700 p-3 rounded">
              <p className="font-bold">Initial Connection</p>
              <p className="text-gray-400 text-sm">Hi [Name], I help businesses...</p>
            </div>
            <div className="bg-gray-700 p-3 rounded">
              <p className="font-bold">Follow Up</p>
              <p className="text-gray-400 text-sm">Just checking if you saw...</p>
            </div>
          </div>
        </div>
        <div className="bg-gray-800 p-4 rounded-lg">
          <h2 className="text-lg font-bold mb-3">📊 Performance</h2>
          <div className="space-y-2">
            <div className="flex justify-between">
              <span>Open Rate</span>
              <span className="text-green-400">71%</span>
            </div>
            <div className="flex justify-between">
              <span>Response Rate</span>
              <span className="text-blue-400">18%</span>
            </div>
            <div className="flex justify-between">
              <span>Connection Accept</span>
              <span className="text-purple-400">42%</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}