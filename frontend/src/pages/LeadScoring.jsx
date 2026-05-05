import { useState, useEffect } from 'react';

const API = import.meta.env.VITE_API_URL || 'https://dmcashield-agency.vercel.app';

export default function LeadScoring() {
  const [leads, setLeads] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API}/api/leads/scored`)
      .then(r => r.json())
      .then(d => { setLeads(d); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  const getScoreColor = (score) => {
    if (score >= 80) return '#10b981';
    if (score >= 60) return '#3b82f6';
    if (score >= 40) return '#f59e0b';
    return '#ef4444';
  };

  const getTempIcon = (temp) => {
    if (temp === 'hot') return '🔥';
    if (temp === 'warm') return '🌡️';
    return '❄️';
  };

  if (loading) return <div className="p-6">Loading...</div>;

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">🎯 Lead Scoring</h1>

      <div className="grid grid-cols-3 gap-4 mb-6">
        <div className="bg-gray-800 p-4 rounded-lg text-center">
          <p className="text-gray-400 text-sm">Hot Leads</p>
          <p className="text-3xl font-bold text-orange-400">{leads.filter(l => l.lead_temperature === 'hot').length}</p>
        </div>
        <div className="bg-gray-800 p-4 rounded-lg text-center">
          <p className="text-gray-400 text-sm">Warm Leads</p>
          <p className="text-3xl font-bold text-blue-400">{leads.filter(l => l.lead_temperature === 'warm').length}</p>
        </div>
        <div className="bg-gray-800 p-4 rounded-lg text-center">
          <p className="text-gray-400 text-sm">Cold Leads</p>
          <p className="text-3xl font-bold text-gray-400">{leads.filter(l => l.lead_temperature === 'cold').length}</p>
        </div>
      </div>

      <div className="bg-gray-800 rounded-lg overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-700">
            <tr>
              <th className="p-3 text-left">Business</th>
              <th className="p-3 text-left">Niche</th>
              <th className="p-3 text-left">City</th>
              <th className="p-3 text-left">Score</th>
              <th className="p-3 text-left">Temperature</th>
              <th className="p-3 text-left">Emails Sent</th>
            </tr>
          </thead>
          <tbody>
            {leads.map(lead => (
              <tr key={lead.id} className="border-t border-gray-700 hover:bg-gray-750">
                <td className="p-3 font-bold">{lead.business_name}</td>
                <td className="p-3">{lead.niche}</td>
                <td className="p-3">{lead.city}</td>
                <td className="p-3">
                  <div className="flex items-center gap-2">
                    <div className="w-16 bg-gray-700 rounded-full h-2">
                      <div style={{ width: `${lead.lead_score}%`, backgroundColor: getScoreColor(lead.lead_score) }} className="h-2 rounded-full"></div>
                    </div>
                    <span style={{ color: getScoreColor(lead.lead_score) }}>{lead.lead_score}</span>
                  </div>
                </td>
                <td className="p-3">
                  <span className="text-lg">{getTempIcon(lead.lead_temperature)}</span>
                </td>
                <td className="p-3">{lead.emails_sent_count}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="mt-6 bg-gray-800 p-4 rounded-lg">
        <h2 className="text-lg font-bold mb-3">📊 Scoring Criteria</h2>
        <div className="grid grid-cols-2 gap-4 text-sm">
          <div className="bg-gray-700 p-3 rounded">
            <p className="text-green-400 font-bold">High Score (80-100):</p>
            <p className="text-gray-400">Hot leads with 3+ negative reviews, good rating, owner info verified</p>
          </div>
          <div className="bg-gray-700 p-3 rounded">
            <p className="text-blue-400 font-bold">Medium Score (60-79):</p>
            <p className="text-gray-400">Warm leads with 1-2 negative reviews, partial data</p>
          </div>
          <div className="bg-gray-700 p-3 rounded">
            <p className="text-yellow-400 font-bold">Low Score (40-59):</p>
            <p className="text-gray-400">Needs validation, missing data, or low review count</p>
          </div>
          <div className="bg-gray-700 p-3 rounded">
            <p className="text-red-400 font-bold">Below 40:</p>
            <p className="text-gray-400">Cold leads, no negative reviews, or invalid data</p>
          </div>
        </div>
      </div>
    </div>
  );
}