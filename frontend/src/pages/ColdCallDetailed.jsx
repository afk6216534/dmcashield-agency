import { useState } from 'react';

export default function ColdCallDetailed() {
  const [calls, setCalls] = useState([
    { id: 1, lead: 'Smile Dental', result: 'interested', duration: '3:45', date: 'Today' },
    { id: 2, lead: 'Houston Auto', result: 'callback', duration: '2:10', date: 'Today' },
    { id: 3, lead: 'Legal Eagles', result: 'closed', duration: '5:20', date: 'Yesterday' },
  ]);

  const getResultColor = (result) => {
    if (result === 'closed') return '#10b981';
    if (result === 'interested') return '#3b82f6';
    if (result === 'callback') return '#f59e0b';
    return '#6b7280';
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">📞 Cold Calling Center</h1>

      <div className="grid grid-cols-4 gap-4 mb-6">
        <div className="bg-gradient-to-br from-blue-600 to-blue-800 p-6 rounded-xl">
          <p className="text-blue-200 text-sm">Calls Today</p>
          <p className="text-3xl font-bold">12</p>
        </div>
        <div className="bg-gradient-to-br from-green-600 to-green-800 p-6 rounded-xl">
          <p className="text-green-200 text-sm">Connected</p>
          <p className="text-3xl font-bold">8</p>
        </div>
        <div className="bg-gradient-to-br from-purple-600 to-purple-800 p-6 rounded-xl">
          <p className="text-purple-200 text-sm">Interested</p>
          <p className="text-3xl font-bold">3</p>
        </div>
        <div className="bg-gradient-to-br from-orange-600 to-orange-800 p-6 rounded-xl">
          <p className="text-orange-200 text-sm">Avg Duration</p>
          <p className="text-3xl font-bold">3:12</p>
        </div>
      </div>

      <div className="bg-gray-800 p-4 rounded-lg mb-6">
        <h2 className="text-lg font-bold mb-4">📋 Recent Calls</h2>
        <div className="space-y-2">
          {calls.map(call => (
            <div key={call.id} className="bg-gray-700 p-3 rounded flex justify-between items-center">
              <div>
                <p className="font-bold">{call.lead}</p>
                <p className="text-gray-400 text-sm">{call.duration} • {call.date}</p>
              </div>
              <span style={{ color: getResultColor(call.result) }} className="font-bold capitalize">
                {call.result}
              </span>
            </div>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-2 gap-6">
        <div className="bg-gray-800 p-4 rounded-lg">
          <h2 className="text-lg font-bold mb-3">📝 Call Scripts</h2>
          <div className="space-y-2">
            <div className="bg-gray-700 p-3 rounded">
              <p className="font-bold">Opening</p>
              <p className="text-gray-400 text-sm">Hi, this is [Name] from DMCAShield...</p>
            </div>
            <div className="bg-gray-700 p-3 rounded">
              <p className="font-bold">Value Prop</p>
              <p className="text-gray-400 text-sm">We help remove negative reviews...</p>
            </div>
            <div className="bg-gray-700 p-3 rounded">
              <p className="font-bold">Closing</p>
              <p className="text-gray-400 text-sm">Can we schedule a demo?</p>
            </div>
          </div>
        </div>
        <div className="bg-gray-800 p-4 rounded-lg">
          <h2 className="text-lg font-bold mb-3">🎯 Best Times</h2>
          <div className="space-y-2 text-sm">
            <div className="flex justify-between bg-gray-700 p-2 rounded">
              <span>Mon-Tue 9-11am</span>
              <span className="text-green-400">Best</span>
            </div>
            <div className="flex justify-between bg-gray-700 p-2 rounded">
              <span>Wed-Thu 2-4pm</span>
              <span className="text-blue-400">Good</span>
            </div>
            <div className="flex justify-between bg-gray-700 p-2 rounded">
              <span>Fri 10-12pm</span>
              <span className="text-yellow-400">Ok</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}