import { useState } from 'react';

export default function AuditLog() {
  const [logs, setLogs] = useState([
    { id: 1, action: 'Task Created', user: 'System', target: 'Dentist LA Campaign', time: '2 min ago' },
    { id: 2, action: 'Lead Updated', user: 'System', target: 'Smile Dental', time: '15 min ago' },
    { id: 3, action: 'Email Sent', user: 'SendHead', target: '45 leads', time: '1 hour ago' },
    { id: 4, action: 'Client Added', user: 'Admin', target: 'Houston Auto', time: '2 hours ago' },
    { id: 5, action: 'Settings Updated', user: 'Admin', target: 'Email limits', time: '3 hours ago' },
  ]);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">🔒 Audit Log</h1>

      <div className="grid grid-cols-4 gap-4 mb-6">
        <div className="bg-gray-800 p-4 rounded-lg text-center">
          <p className="text-gray-400 text-sm">Total Events</p>
          <p className="text-2xl font-bold">1,247</p>
        </div>
        <div className="bg-gray-800 p-4 rounded-lg text-center">
          <p className="text-gray-400 text-sm">Today</p>
          <p className="text-2xl font-bold text-blue-400">23</p>
        </div>
        <div className="bg-gray-800 p-4 rounded-lg text-center">
          <p className="text-gray-400 text-sm">Errors</p>
          <p className="text-2xl font-bold text-red-400">2</p>
        </div>
        <div className="bg-gray-800 p-4 rounded-lg text-center">
          <p className="text-gray-400 text-sm">Warnings</p>
          <p className="text-2xl font-bold text-yellow-400">5</p>
        </div>
      </div>

      <div className="bg-gray-800 rounded-lg overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-700">
            <tr>
              <th className="p-3 text-left">Action</th>
              <th className="p-3 text-left">User</th>
              <th className="p-3 text-left">Target</th>
              <th className="p-3 text-left">Time</th>
            </tr>
          </thead>
          <tbody>
            {logs.map(log => (
              <tr key={log.id} className="border-t border-gray-700 hover:bg-gray-750">
                <td className="p-3 font-bold">{log.action}</td>
                <td className="p-3 text-gray-400">{log.user}</td>
                <td className="p-3">{log.target}</td>
                <td className="p-3 text-gray-500 text-sm">{log.time}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="mt-6 bg-gray-800 p-4 rounded-lg">
        <h2 className="text-lg font-bold mb-3">⚙️ Log Settings</h2>
        <div className="space-y-2">
          <label className="flex items-center gap-2">
            <input type="checkbox" defaultChecked />
            <span>Log all user actions</span>
          </label>
          <label className="flex items-center gap-2">
            <input type="checkbox" defaultChecked />
            <span>Log system events</span>
          </label>
          <label className="flex items-center gap-2">
            <input type="checkbox" defaultChecked />
            <span>Log API calls</span>
          </label>
          <label className="flex items-center gap-2">
            <input type="checkbox" />
            <span>Log failed attempts only</span>
          </label>
        </div>
      </div>
    </div>
  );
}