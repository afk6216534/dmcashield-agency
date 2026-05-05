import { useState } from 'react';

const API = import.meta.env.VITE_API_URL || 'https://dmcashield-agency.vercel.app';

export default function QuickLaunch() {
  const [form, setForm] = useState({
    business_type: 'dentist',
    city: '',
    state: '',
    country: 'USA',
    niche: ''
  });
  const [launching, setLaunching] = useState(false);
  const [result, setResult] = useState(null);

  const niches = [
    { value: 'dentist', label: 'Dentist / Dental Clinic' },
    { value: 'clinic', label: 'Medical Clinic' },
    { value: 'lawyer', label: 'Law Firm / Attorney' },
    { value: 'plumber', label: 'Plumber' },
    { value: 'electrician', label: 'Electrician' },
    { value: 'hvac', label: 'HVAC / Heating & Cooling' },
    { value: 'restaurant', label: 'Restaurant' },
    { value: 'gym', label: 'Gym / Fitness Center' },
    { value: 'salon', label: 'Salon / Spa' },
    { value: 'auto', label: 'Auto Repair' },
  ];

  const launchTask = async () => {
    if (!form.city || !form.state) {
      alert('Please enter city and state');
      return;
    }
    setLaunching(true);
    try {
      const res = await fetch(`${API}/api/tasks`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form)
      });
      const data = await res.json();
      setResult(data);
    } catch (e) {
      setResult({ error: 'Failed to launch task' });
    }
    setLaunching(false);
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">🚀 Quick Launch</h1>

      <div className="grid grid-cols-2 gap-6">
        <div className="bg-gray-800 p-6 rounded-lg">
          <h2 className="text-lg font-bold mb-4">Launch New Campaign</h2>
          
          <div className="space-y-4">
            <div>
              <label className="block text-gray-400 mb-2">Business Type</label>
              <select value={form.business_type} onChange={e => setForm({...form, business_type: e.target.value, niche: e.target.value})}
                className="w-full bg-gray-700 text-white p-2 rounded">
                {niches.map(n => <option key={n.value} value={n.value}>{n.label}</option>)}
              </select>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-gray-400 mb-2">City *</label>
                <input value={form.city} onChange={e => setForm({...form, city: e.target.value})}
                  className="w-full bg-gray-700 text-white p-2 rounded" placeholder="e.g., Los Angeles" />
              </div>
              <div>
                <label className="block text-gray-400 mb-2">State *</label>
                <input value={form.state} onChange={e => setForm({...form, state: e.target.value})}
                  className="w-full bg-gray-700 text-white p-2 rounded" placeholder="e.g., CA" />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-gray-400 mb-2">Country</label>
                <input value={form.country} onChange={e => setForm({...form, country: e.target.value})}
                  className="w-full bg-gray-700 text-white p-2 rounded" />
              </div>
              <div>
                <label className="block text-gray-400 mb-2">Leads Target</label>
                <input type="number" defaultValue={50}
                  className="w-full bg-gray-700 text-white p-2 rounded" />
              </div>
            </div>

            <button onClick={launchTask} disabled={launching}
              className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white py-3 rounded-lg font-bold hover:from-blue-700 hover:to-purple-700 disabled:opacity-50">
              {launching ? 'Launching...' : '🚀 Launch Campaign'}
            </button>
          </div>

          {result && (
            <div className={`mt-4 p-4 rounded ${result.error ? 'bg-red-900' : 'bg-green-900'}`}>
              {result.error ? (
                <p className="text-red-400">{result.error}</p>
              ) : (
                <div>
                  <p className="text-green-400 font-bold">✅ Campaign Launched!</p>
                  <p className="text-sm text-gray-300">Task ID: {result.task_id}</p>
                  <p className="text-sm text-gray-300">Phase: {result.phase}</p>
                </div>
              )}
            </div>
          )}
        </div>

        <div className="space-y-4">
          <div className="bg-gray-800 p-4 rounded-lg">
            <h3 className="font-bold mb-3">📊 Campaign Workflow</h3>
            <div className="space-y-2 text-sm">
              <div className="flex items-center gap-2">
                <span className="bg-blue-600 px-2 py-1 rounded">1</span>
                <span>Scraping - Find businesses with negative reviews</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="bg-blue-600 px-2 py-1 rounded">2</span>
                <span>Validation - Verify contact info & score leads</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="bg-blue-600 px-2 py-1 rounded">3</span>
                <span>Marketing - Create personalized email funnel</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="bg-blue-600 px-2 py-1 rounded">4</span>
                <span>Sending - Send 6-email sequence</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="bg-blue-600 px-2 py-1 rounded">5</span>
                <span>Tracking - Monitor opens, clicks, replies</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="bg-blue-600 px-2 py-1 rounded">6</span>
                <span>Sales - Convert hot leads to DMCA clients</span>
              </div>
            </div>
          </div>

          <div className="bg-gray-800 p-4 rounded-lg">
            <h3 className="font-bold mb-3">🎯 Expected Results</h3>
            <div className="grid grid-cols-3 gap-2 text-center text-sm">
              <div className="bg-gray-700 p-2 rounded">
                <p className="text-2xl font-bold">50</p>
                <p className="text-gray-400">Leads</p>
              </div>
              <div className="bg-gray-700 p-2 rounded">
                <p className="text-2xl font-bold text-orange-400">8-12</p>
                <p className="text-gray-400">Hot Leads</p>
              </div>
              <div className="bg-gray-700 p-2 rounded">
                <p className="text-2xl font-bold text-green-400">2-4</p>
                <p className="text-gray-400">Conversions</p>
              </div>
            </div>
          </div>

          <div className="bg-gray-800 p-4 rounded-lg">
            <h3 className="font-bold mb-3">⚡ Quick Tips</h3>
            <ul className="text-sm text-gray-400 space-y-1">
              <li>• Target cities with population 100k+</li>
              <li>• Focus on businesses with 3+ negative reviews</li>
              <li>• Monday-Tuesday morning launches work best</li>
              <li>• Watch hot leads in real-time</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}