import { useState } from 'react';

export default function Pipeline() {
  const [stages] = useState([
    { id: 'lead', name: 'New Leads', color: '#3b82f6', count: 45 },
    { id: 'contacted', name: 'Contacted', color: '#8b5cf6', count: 32 },
    { id: 'qualified', name: 'Qualified', color: '#f59e0b', count: 18 },
    { id: 'proposal', name: 'Proposal Sent', color: '#ec4899', count: 8 },
    { id: 'closed', name: 'Closed Won', color: '#10b981', count: 5 },
  ]);

  const [deals] = useState([
    { id: 1, name: 'Smile Dental Clinic', value: 2500, stage: 'proposal', owner: 'John' },
    { id: 2, name: 'Houston Auto', value: 1500, stage: 'qualified', owner: 'Sarah' },
    { id: 3, name: 'Legal Eagles', value: 3000, stage: 'closed', owner: 'Mike' },
    { id: 4, name: 'Pizza Palace', value: 1000, stage: 'contacted', owner: 'John' },
    { id: 5, name: 'Bright Eyes', value: 2000, stage: 'lead', owner: 'Sarah' },
  ]);

  const totalValue = deals.reduce((a, d) => a + d.value, 0);
  const wonValue = deals.filter(d => d.stage === 'closed').reduce((a, d) => a + d.value, 0);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">📊 Sales Pipeline</h1>

      <div className="grid grid-cols-4 gap-4 mb-6">
        <div className="bg-gradient-to-br from-blue-600 to-blue-800 p-6 rounded-xl">
          <p className="text-blue-200 text-sm">Total Deals</p>
          <p className="text-3xl font-bold">{deals.length}</p>
        </div>
        <div className="bg-gradient-to-br from-green-600 to-green-800 p-6 rounded-xl">
          <p className="text-green-200 text-sm">Pipeline Value</p>
          <p className="text-3xl font-bold">${totalValue.toLocaleString()}</p>
        </div>
        <div className="bg-gradient-to-br from-purple-600 to-purple-800 p-6 rounded-xl">
          <p className="text-purple-200 text-sm">Won This Month</p>
          <p className="text-3xl font-bold">${wonValue.toLocaleString()}</p>
        </div>
        <div className="bg-gradient-to-br from-orange-600 to-orange-800 p-6 rounded-xl">
          <p className="text-orange-200 text-sm">Win Rate</p>
          <p className="text-3xl font-bold">{Math.round(wonValue / totalValue * 100)}%</p>
        </div>
      </div>

      <div className="grid grid-cols-5 gap-4">
        {stages.map(stage => (
          <div key={stage.id} className="bg-gray-800 rounded-lg">
            <div className="p-3 border-b border-gray-700" style={{ borderTop: `3px solid ${stage.color}` }}>
              <h3 className="font-bold">{stage.name}</h3>
              <p className="text-gray-400 text-sm">{stage.count} deals</p>
            </div>
            <div className="p-2 space-y-2">
              {deals.filter(d => d.stage === stage.id).map(deal => (
                <div key={deal.id} className="bg-gray-700 p-2 rounded text-sm">
                  <p className="font-bold truncate">{deal.name}</p>
                  <p className="text-green-400">${deal.value.toLocaleString()}</p>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}