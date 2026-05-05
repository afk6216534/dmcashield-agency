import { useState, useEffect } from 'react';

const API = import.meta.env.VITE_API_URL || 'https://dmcashield-agency.vercel.app';

export default function DMCATracker() {
  const [cases, setCases] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [newCase, setNewCase] = useState({ client_name: '', platform: 'Google' });

  useEffect(() => {
    fetch(`${API}/api/dmca/cases`)
      .then(r => r.json())
      .then(d => { setCases(d); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  const createCase = async () => {
    const res = await fetch(`${API}/api/dmca/cases`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newCase)
    });
    const data = await res.json();
    setCases([...cases, { ...newCase, id: data.id, status: 'submitted', negative_reviews_removed: 0, submitted_at: new Date().toISOString() }]);
    setShowForm(false);
    setNewCase({ client_name: '', platform: 'Google' });
  };

  const getStatusColor = (status) => {
    if (status === 'completed') return '#10b981';
    if (status === 'under_review') return '#f59e0b';
    return '#3b82f6';
  };

  if (loading) return <div className="p-6">Loading...</div>;

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">DMCA Case Tracker</h1>
        <button onClick={() => setShowForm(!showForm)} className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
          + New Case
        </button>
      </div>

      {showForm && (
        <div className="bg-gray-800 p-4 rounded-lg mb-6">
          <div className="grid grid-cols-2 gap-4">
            <input placeholder="Client Name" value={newCase.client_name} onChange={e => setNewCase({...newCase, client_name: e.target.value})}
              className="bg-gray-700 text-white p-2 rounded" />
            <select value={newCase.platform} onChange={e => setNewCase({...newCase, platform: e.target.value})}
              className="bg-gray-700 text-white p-2 rounded">
              <option>Google</option>
              <option>Yelp</option>
              <option>Trustpilot</option>
              <option>Facebook</option>
            </select>
          </div>
          <button onClick={createCase} className="mt-4 bg-green-600 text-white px-4 py-2 rounded">Submit Case</button>
        </div>
      )}

      <div className="grid gap-4">
        {cases.map(caseItem => (
          <div key={caseItem.id} className="bg-gray-800 p-4 rounded-lg flex justify-between items-center">
            <div>
              <h3 className="font-bold text-lg">{caseItem.client_name}</h3>
              <p className="text-gray-400">{caseItem.platform} • Submitted: {new Date(caseItem.submitted_at).toLocaleDateString()}</p>
            </div>
            <div className="text-right">
              <span style={{ color: getStatusColor(caseItem.status), fontWeight: 'bold' }}>{caseItem.status.replace('_', ' ').toUpperCase()}</span>
              <p className="text-gray-400">{caseItem.negative_reviews_removed} removed</p>
            </div>
          </div>
        ))}
      </div>

      {cases.length === 0 && <p className="text-gray-400 text-center py-8">No DMCA cases yet</p>}
    </div>
  );
}