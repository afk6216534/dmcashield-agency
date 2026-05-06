import { useState } from 'react';

export default function Widgets() {
  const [widgets, setWidgets] = useState([
    { id: 1, type: 'stats', name: 'Quick Stats', enabled: true },
    { id: 2, type: 'chart', name: 'Email Performance', enabled: true },
    { id: 3, type: 'list', name: 'Hot Leads', enabled: true },
    { id: 4, type: 'activity', name: 'Recent Activity', enabled: false },
  ]);

  const toggleWidget = (id) => {
    setWidgets(widgets.map(w => w.id === id ? { ...w, enabled: !w.enabled } : w));
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">🧩 Dashboard Widgets</h1>

      <div className="bg-gray-800 rounded-lg overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-700">
            <tr>
              <th className="p-3 text-left">Widget</th>
              <th className="p-3 text-left">Type</th>
              <th className="p-3 text-left">Status</th>
              <th className="p-3 text-left">Actions</th>
            </tr>
          </thead>
          <tbody>
            {widgets.map(w => (
              <tr key={w.id} className="border-t border-gray-700">
                <td className="p-3 font-bold">{w.name}</td>
                <td className="p-3 text-gray-400 capitalize">{w.type}</td>
                <td className="p-3">
                  <span className={`px-2 py-1 rounded text-sm ${w.enabled ? 'bg-green-900 text-green-400' : 'bg-gray-600'}`}>
                    {w.enabled ? 'Active' : 'Disabled'}
                  </span>
                </td>
                <td className="p-3">
                  <button onClick={() => toggleWidget(w.id)} className="bg-blue-600 px-3 py-1 rounded text-sm">
                    {w.enabled ? 'Disable' : 'Enable'}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="mt-6 grid grid-cols-2 gap-4">
        <div className="bg-gray-800 p-4 rounded-lg">
          <h2 className="font-bold mb-3">Available Widgets</h2>
          <p className="text-gray-400 text-sm">Drag and drop widgets to customize your dashboard layout.</p>
        </div>
        <div className="bg-gray-800 p-4 rounded-lg">
          <h2 className="font-bold mb-3">Widget Settings</h2>
          <p className="text-gray-400 text-sm">Click on any widget to configure its display options.</p>
        </div>
      </div>
    </div>
  );
}