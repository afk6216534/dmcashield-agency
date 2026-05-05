import { useState, useEffect } from 'react';

const API = import.meta.env.VITE_API_URL || 'https://dmcashield-agency.vercel.app';

export default function LeadDetailed() {
  const [leads, setLeads] = useState([]);
  const [selectedLead, setSelectedLead] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API}/api/leads`)
      .then(r => r.json())
      .then(d => { setLeads(d); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  const viewLead = async (id) => {
    const res = await fetch(`${API}/api/leads/${id}`);
    const data = await res.json();
    setSelectedLead(data);
  };

  const getTempColor = (temp) => {
    if (temp === 'hot') return '#ef4444';
    if (temp === 'warm') return '#f59e0b';
    return '#3b82f6';
  };

  const getStatusColor = (status) => {
    if (status === 'replied') return '#10b981';
    if (status === 'funnel_ready') return '#3b82f6';
    if (status === 'emailed') return '#f59e0b';
    return '#6b7280';
  };

  if (loading) return <div className="p-6">Loading...</div>;

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">👥 Lead Database - Detailed</h1>

      <div className="grid grid-cols-4 gap-4 mb-6">
        <div className="bg-gray-800 p-4 rounded-lg text-center">
          <p className="text-gray-400 text-sm">Total Leads</p>
          <p className="text-2xl font-bold">{leads.length}</p>
        </div>
        <div className="bg-gray-800 p-4 rounded-lg text-center">
          <p className="text-gray-400 text-sm">Hot</p>
          <p className="text-2xl font-bold text-red-400">{leads.filter(l => l.lead_temperature === 'hot').length}</p>
        </div>
        <div className="bg-gray-800 p-4 rounded-lg text-center">
          <p className="text-gray-400 text-sm">Warm</p>
          <p className="text-2xl font-bold text-yellow-400">{leads.filter(l => l.lead_temperature === 'warm').length}</p>
        </div>
        <div className="bg-gray-800 p-4 rounded-lg text-center">
          <p className="text-gray-400 text-sm">Cold</p>
          <p className="text-2xl font-bold text-blue-400">{leads.filter(l => l.lead_temperature === 'cold').length}</p>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-6">
        <div className="col-span-2 bg-gray-800 rounded-lg overflow-hidden">
          <table className="w-full">
            <thead className="bg-gray-700">
              <tr>
                <th className="p-3 text-left">Business</th>
                <th className="p-3 text-left">Owner</th>
                <th className="p-3 text-left">City</th>
                <th className="p-3 text-left">Temp</th>
                <th className="p-3 text-left">Status</th>
                <th className="p-3 text-left">Score</th>
                <th className="p-3 text-left">Action</th>
              </tr>
            </thead>
            <tbody>
              {leads.map(lead => (
                <tr key={lead.id} className="border-t border-gray-700 hover:bg-gray-750">
                  <td className="p-3 font-bold">{lead.business_name}</td>
                  <td className="p-3">{lead.owner_name}</td>
                  <td className="p-3">{lead.city}, {lead.state}</td>
                  <td className="p-3">
                    <span style={{ color: getTempColor(lead.lead_temperature) }} className="font-bold">
                      {lead.lead_temperature.toUpperCase()}
                    </span>
                  </td>
                  <td className="p-3">
                    <span style={{ color: getStatusColor(lead.status) }} className="text-sm">
                      {lead.status}
                    </span>
                  </td>
                  <td className="p-3">
                    <span className={`font-bold ${lead.lead_score >= 80 ? 'text-green-400' : lead.lead_score >= 60 ? 'text-blue-400' : 'text-gray-400'}`}>
                      {lead.lead_score}
                    </span>
                  </td>
                  <td className="p-3">
                    <button onClick={() => viewLead(lead.id)} className="bg-blue-600 px-2 py-1 rounded text-sm">View</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="bg-gray-800 p-4 rounded-lg">
          <h2 className="text-lg font-bold mb-3">📊 Lead Details</h2>
          {selectedLead ? (
            <div className="space-y-3">
              <div className="bg-gray-700 p-3 rounded">
                <p className="text-gray-400 text-sm">Business</p>
                <p className="font-bold">{selectedLead.business_name}</p>
              </div>
              <div className="bg-gray-700 p-3 rounded">
                <p className="text-gray-400 text-sm">Owner</p>
                <p className="font-bold">{selectedLead.owner_name}</p>
              </div>
              <div className="bg-gray-700 p-3 rounded">
                <p className="text-gray-400 text-sm">Email</p>
                <p className="font-bold">{selectedLead.email_primary}</p>
              </div>
              <div className="bg-gray-700 p-3 rounded">
                <p className="text-gray-400 text-sm">Phone</p>
                <p className="font-bold">{selectedLead.phone}</p>
              </div>
              <div className="bg-gray-700 p-3 rounded">
                <p className="text-gray-400 text-sm">Niche</p>
                <p className="font-bold capitalize">{selectedLead.niche}</p>
              </div>
              <div className="bg-gray-700 p-3 rounded">
                <p className="text-gray-400 text-sm">Rating</p>
                <p className="font-bold">{selectedLead.current_rating} ⭐</p>
              </div>
              <div className="bg-gray-700 p-3 rounded">
                <p className="text-gray-400 text-sm">Negative Reviews</p>
                <p className="font-bold text-red-400">{selectedLead.negative_review_count}</p>
              </div>
              <div className="bg-gray-700 p-3 rounded">
                <p className="text-gray-400 text-sm">Funnel Step</p>
                <p className="font-bold">Step {selectedLead.funnel_step}/5</p>
              </div>
              
              {selectedLead.email_history && (
                <div className="mt-4">
                  <h3 className="font-bold mb-2">📧 Email History</h3>
                  {selectedLead.email_history.map((email, i) => (
                    <div key={i} className="bg-gray-700 p-2 rounded mb-2 text-sm">
                      <p className="font-bold">#{email.email_number}: {email.subject_line}</p>
                      <p className="text-gray-400">
                        {email.opened ? '✅ Opened' : '❌ Not opened'} • 
                        {email.replied ? ' ✅ Replied' : ' ❌ No reply'}
                      </p>
                    </div>
                  ))}
                </div>
              )}
            </div>
          ) : (
            <p className="text-gray-400 text-center py-8">Click "View" to see lead details</p>
          )}
        </div>
      </div>
    </div>
  );
}