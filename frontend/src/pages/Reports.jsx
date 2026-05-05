import { useState } from 'react';

export default function Reports() {
  const [period, setPeriod] = useState('week');

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">📊 Reports & Exports</h1>
        <select value={period} onChange={e => setPeriod(e.target.value)} className="bg-gray-700 text-white p-2 rounded">
          <option value="week">This Week</option>
          <option value="month">This Month</option>
          <option value="quarter">This Quarter</option>
          <option value="year">This Year</option>
        </select>
      </div>

      <div className="grid grid-cols-3 gap-4 mb-6">
        <div className="bg-gray-800 p-4 rounded-lg">
          <h3 className="font-bold mb-3">📧 Email Reports</h3>
          <div className="space-y-2">
            <button className="w-full bg-blue-600 py-2 rounded text-sm">Download CSV</button>
            <button className="w-full bg-blue-600 py-2 rounded text-sm">Download PDF</button>
          </div>
        </div>
        <div className="bg-gray-800 p-4 rounded-lg">
          <h3 className="font-bold mb-3">👥 Lead Reports</h3>
          <div className="space-y-2">
            <button className="w-full bg-green-600 py-2 rounded text-sm">Export Leads</button>
            <button className="w-full bg-green-600 py-2 rounded text-sm">Score Report</button>
          </div>
        </div>
        <div className="bg-gray-800 p-4 rounded-lg">
          <h3 className="font-bold mb-3">💰 Revenue Reports</h3>
          <div className="space-y-2">
            <button className="w-full bg-purple-600 py-2 rounded text-sm">Monthly Sales</button>
            <button className="w-full bg-purple-600 py-2 rounded text-sm">Client List</button>
          </div>
        </div>
      </div>

      <div className="bg-gray-800 p-4 rounded-lg">
        <h2 className="text-lg font-bold mb-3">📈 Performance Summary</h2>
        <div className="grid grid-cols-4 gap-4">
          <div className="bg-gray-700 p-3 rounded text-center">
            <p className="text-2xl font-bold">247</p>
            <p className="text-gray-400 text-sm">Total Leads</p>
          </div>
          <div className="bg-gray-700 p-3 rounded text-center">
            <p className="text-2xl font-bold">1,247</p>
            <p className="text-gray-400 text-sm">Emails Sent</p>
          </div>
          <div className="bg-gray-700 p-3 rounded text-center">
            <p className="text-2xl font-bold">38</p>
            <p className="text-gray-400 text-sm">Hot Leads</p>
          </div>
          <div className="bg-gray-700 p-3 rounded text-center">
            <p className="text-2xl font-bold">$12,500</p>
            <p className="text-gray-400 text-sm">Revenue</p>
          </div>
        </div>
      </div>

      <div className="mt-6 bg-gray-800 p-4 rounded-lg">
        <h2 className="text-lg font-bold mb-3">🕐 Scheduled Reports</h2>
        <div className="space-y-2">
          <div className="flex justify-between items-center bg-gray-700 p-3 rounded">
            <span>Weekly Summary</span>
            <span className="text-gray-400">Every Monday 9am</span>
            <span className="text-green-400">Active</span>
          </div>
          <div className="flex justify-between items-center bg-gray-700 p-3 rounded">
            <span>Monthly Performance</span>
            <span className="text-gray-400">1st of month</span>
            <span className="text-green-400">Active</span>
          </div>
        </div>
        <button className="mt-3 bg-blue-600 px-4 py-2 rounded text-sm">+ Schedule Report</button>
      </div>
    </div>
  );
}