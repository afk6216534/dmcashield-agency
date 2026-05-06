import { useState } from 'react';

export default function Changelog() {
  const [versions] = useState([
    { version: '4.8.0', date: 'May 5, 2026', changes: ['Added Pipeline (CRM)', 'Added Kanban Board'] },
    { version: '4.7.0', date: 'May 5, 2026', changes: ['Added White Label', 'Added API Docs'] },
    { version: '4.6.0', date: 'May 5, 2026', changes: ['Added Help Center', 'Added Client Portal', 'Added Landing Page'] },
    { version: '4.5.0', date: 'May 5, 2026', changes: ['Added System Health', 'Added Overview page'] },
    { version: '4.0.0', date: 'May 5, 2026', changes: ['Major update - 47 pages total', 'Complete system overhaul'] },
    { version: '3.0.0', date: 'May 1, 2026', changes: ['Initial launch', 'Basic dashboard'] },
  ]);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">📝 Changelog</h1>

      <div className="space-y-4">
        {versions.map((v, i) => (
          <div key={i} className="bg-gray-800 rounded-lg overflow-hidden">
            <div className="p-4 border-l-4 border-blue-500">
              <div className="flex justify-between items-center mb-2">
                <span className="text-xl font-bold">v{v.version}</span>
                <span className="text-gray-400 text-sm">{v.date}</span>
              </div>
              <ul className="space-y-1">
                {v.changes.map((c, j) => (
                  <li key={j} className="text-gray-300">• {c}</li>
                ))}
              </ul>
            </div>
          </div>
        ))}
      </div>

      <div className="mt-6 bg-gray-800 p-4 rounded-lg">
        <h2 className="font-bold mb-3">🚀 Coming Soon</h2>
        <ul className="text-gray-400 text-sm space-y-1">
          <li>• Mobile app</li>
          <li>• Slack integration</li>
          <li>• A/B testing for emails</li>
          <li>• Custom workflows</li>
        </ul>
      </div>
    </div>
  );
}