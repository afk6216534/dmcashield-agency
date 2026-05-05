import { useState, useEffect } from 'react';

const API = import.meta.env.VITE_API_URL || 'https://dmcashield-agency.vercel.app';

export default function SettingsDetailed() {
  const [settings, setSettings] = useState(null);
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    fetch(`${API}/api/settings`)
      .then(r => r.json())
      .then(d => setSettings(d))
      .catch(() => {});
  }, []);

  const saveSettings = async () => {
    setSaving(true);
    await fetch(`${API}/api/settings`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(settings)
    });
    setSaving(false);
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  if (!settings) return <div className="p-6">Loading...</div>;

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">⚙️ System Settings</h1>
        <button onClick={saveSettings} disabled={saving}
          className={`px-4 py-2 rounded font-bold ${saved ? 'bg-green-600' : 'bg-blue-600'} text-white`}>
          {saving ? 'Saving...' : saved ? '✓ Saved!' : 'Save Settings'}
        </button>
      </div>

      <div className="grid grid-cols-2 gap-6">
        <div className="bg-gray-800 p-4 rounded-lg">
          <h2 className="text-lg font-bold mb-4">📡 API Configuration</h2>
          <div className="space-y-4">
            <div>
              <label className="block text-gray-400 mb-2">OpenRouter API Key</label>
              <input type="password" value="sk-or-v1-xxxxx..." 
                className="w-full bg-gray-700 text-white p-2 rounded" />
              <p className="text-xs text-gray-500 mt-1">Get key from openrouter.ai</p>
            </div>
            <div className="flex items-center gap-2">
              <input type="checkbox" checked={settings.openrouter_configured} readOnly />
              <span>OpenRouter Connected</span>
            </div>
          </div>
        </div>

        <div className="bg-gray-800 p-4 rounded-lg">
          <h2 className="text-lg font-bold mb-4">📧 Email Settings</h2>
          <div className="space-y-4">
            <div>
              <label className="block text-gray-400 mb-2">Max Emails Per Day</label>
              <input type="number" value={settings.max_emails_per_day}
                onChange={e => setSettings({...settings, max_emails_per_day: parseInt(e.target.value)})}
                className="w-full bg-gray-700 text-white p-2 rounded" />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-gray-400 mb-2">Min Gap (seconds)</label>
                <input type="number" value={settings.email_gap_min}
                  onChange={e => setSettings({...settings, email_gap_min: parseInt(e.target.value)})}
                  className="w-full bg-gray-700 text-white p-2 rounded" />
              </div>
              <div>
                <label className="block text-gray-400 mb-2">Max Gap (seconds)</label>
                <input type="number" value={settings.email_gap_max}
                  onChange={e => setSettings({...settings, email_gap_max: parseInt(e.target.value)})}
                  className="w-full bg-gray-700 text-white p-2 rounded" />
              </div>
            </div>
          </div>
        </div>

        <div className="bg-gray-800 p-4 rounded-lg">
          <h2 className="text-lg font-bold mb-4">🤖 AI Models</h2>
          <div className="space-y-3">
            {Object.entries(settings.models || {}).map(([key, val]) => (
              <div key={key} className="flex justify-between items-center">
                <span className="capitalize text-gray-400">{key}</span>
                <input value={val} onChange={e => setSettings({
                  ...settings, 
                  models: {...settings.models, [key]: e.target.value}
                })} className="bg-gray-700 text-white p-1 rounded text-sm w-48" />
              </div>
            ))}
          </div>
        </div>

        <div className="bg-gray-800 p-4 rounded-lg">
          <h2 className="text-lg font-bold mb-4">🔒 Security</h2>
          <div className="space-y-3">
            <div className="flex items-center gap-2">
              <input type="checkbox" defaultChecked />
              <span>Encrypt sensitive data</span>
            </div>
            <div className="flex items-center gap-2">
              <input type="checkbox" defaultChecked />
              <span>Audit logging enabled</span>
            </div>
            <div className="flex items-center gap-2">
              <input type="checkbox" defaultChecked />
              <span>Two-factor authentication</span>
            </div>
          </div>
        </div>
      </div>

      <div className="mt-6 bg-gray-800 p-4 rounded-lg">
        <h2 className="text-lg font-bold mb-3">🧪 Test Connections</h2>
        <div className="flex gap-4">
          <button className="bg-gray-700 px-4 py-2 rounded hover:bg-gray-600">Test SMTP</button>
          <button className="bg-gray-700 px-4 py-2 rounded hover:bg-gray-600">Test OpenRouter</button>
          <button className="bg-gray-700 px-4 py-2 rounded hover:bg-gray-600">Test Webhooks</button>
        </div>
      </div>
    </div>
  );
}