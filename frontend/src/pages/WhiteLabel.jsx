import { useState } from 'react';

export default function WhiteLabel() {
  const [settings, setSettings] = useState({
    brand_name: 'DMCAShield',
    brand_color: '#3b82f6',
    logo_url: '',
    favicon_url: '',
    custom_css: '',
    custom_domain: ''
  });

  const saveSettings = () => {
    alert('Settings saved! (Demo)');
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">🎨 White Label Settings</h1>

      <div className="grid grid-cols-2 gap-6">
        <div className="bg-gray-800 p-4 rounded-lg">
          <h2 className="text-lg font-bold mb-4">Brand Settings</h2>
          <div className="space-y-4">
            <div>
              <label className="block text-gray-400 mb-2">Brand Name</label>
              <input value={settings.brand_name} onChange={e => setSettings({...settings, brand_name: e.target.value})}
                className="w-full bg-gray-700 text-white p-2 rounded" />
            </div>
            <div>
              <label className="block text-gray-400 mb-2">Brand Color</label>
              <div className="flex gap-2">
                <input type="color" value={settings.brand_color} onChange={e => setSettings({...settings, brand_color: e.target.value})}
                  className="w-12 h-10 rounded" />
                <input value={settings.brand_color} onChange={e => setSettings({...settings, brand_color: e.target.value})}
                  className="flex-1 bg-gray-700 text-white p-2 rounded" />
              </div>
            </div>
            <div>
              <label className="block text-gray-400 mb-2">Logo URL</label>
              <input value={settings.logo_url} onChange={e => setSettings({...settings, logo_url: e.target.value})}
                className="w-full bg-gray-700 text-white p-2 rounded" placeholder="https://..." />
            </div>
            <div>
              <label className="block text-gray-400 mb-2">Favicon URL</label>
              <input value={settings.favicon_url} onChange={e => setSettings({...settings, favicon_url: e.target.value})}
                className="w-full bg-gray-700 text-white p-2 rounded" placeholder="https://..." />
            </div>
            <div>
              <label className="block text-gray-400 mb-2">Custom Domain</label>
              <input value={settings.custom_domain} onChange={e => setSettings({...settings, custom_domain: e.target.value})}
                className="w-full bg-gray-700 text-white p-2 rounded" placeholder="app.yourdomain.com" />
            </div>
          </div>
        </div>

        <div className="bg-gray-800 p-4 rounded-lg">
          <h2 className="text-lg font-bold mb-4">Preview</h2>
          <div className="bg-gray-700 p-4 rounded" style={{ borderTop: `4px solid ${settings.brand_color}` }}>
            <div className="flex items-center gap-2 mb-4">
              <div className="w-8 h-8 rounded bg-current" style={{ backgroundColor: settings.brand_color }}></div>
              <span className="font-bold">{settings.brand_name}</span>
            </div>
            <p className="text-gray-400 text-sm">This is how your branded dashboard will look to clients.</p>
          </div>
        </div>
      </div>

      <div className="bg-gray-800 p-4 rounded-lg mt-6">
        <h2 className="text-lg font-bold mb-4">Advanced</h2>
        <div className="space-y-4">
          <div>
            <label className="block text-gray-400 mb-2">Custom CSS</label>
            <textarea value={settings.custom_css} onChange={e => setSettings({...settings, custom_css: e.target.value})}
              className="w-full bg-gray-700 text-white p-2 rounded h-32 font-mono text-sm" placeholder=".custom-class { }"></textarea>
          </div>
        </div>
      </div>

      <button onClick={saveSettings} className="mt-6 bg-blue-600 text-white px-6 py-2 rounded font-bold hover:bg-blue-700">
        Save Branding
      </button>
    </div>
  );
}