import { useState } from 'react';

export default function Notifications() {
  const [notifications, setNotifications] = useState([
    { id: 1, type: 'lead', title: 'New Hot Lead', message: 'Smile Dental Clinic is ready for conversion', time: '2 min ago', read: false },
    { id: 2, type: 'campaign', title: 'Campaign Complete', message: 'Dentist Houston campaign finished', time: '1 hour ago', read: false },
    { id: 3, type: 'email', title: 'High Open Rate', message: 'Clinic campaign reached 45% open rate', time: '2 hours ago', read: true },
    { id: 4, type: 'system', title: 'Email Account Ready', message: 'campaign@dmcashield.com warmup complete', time: '3 hours ago', read: true },
    { id: 5, type: 'lead', title: 'Reply Received', message: 'Legal Eagles replied to email #3', time: '5 hours ago', read: true },
  ]);

  const markAllRead = () => {
    setNotifications(notifications.map(n => ({ ...n, read: true })));
  };

  const getIcon = (type) => {
    if (type === 'lead') return '🔥';
    if (type === 'campaign') return '📣';
    if (type === 'email') return '📧';
    return '⚙️';
  };

  const getColor = (type) => {
    if (type === 'lead') return 'text-orange-400';
    if (type === 'campaign') return 'text-blue-400';
    if (type === 'email') return 'text-green-400';
    return 'text-gray-400';
  };

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">🔔 Notifications</h1>
        <button onClick={markAllRead} className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
          Mark all as read
        </button>
      </div>

      <div className="grid grid-cols-4 gap-4 mb-6">
        <div className="bg-gray-800 p-4 rounded-lg text-center">
          <p className="text-gray-400 text-sm">Total</p>
          <p className="text-2xl font-bold">{notifications.length}</p>
        </div>
        <div className="bg-gray-800 p-4 rounded-lg text-center">
          <p className="text-gray-400 text-sm">Unread</p>
          <p className="text-2xl font-bold text-orange-400">{notifications.filter(n => !n.read).length}</p>
        </div>
        <div className="bg-gray-800 p-4 rounded-lg text-center">
          <p className="text-gray-400 text-sm">Today</p>
          <p className="text-2xl font-bold text-blue-400">3</p>
        </div>
        <div className="bg-gray-800 p-4 rounded-lg text-center">
          <p className="text-gray-400 text-sm">This Week</p>
          <p className="text-2xl font-bold text-green-400">12</p>
        </div>
      </div>

      <div className="bg-gray-800 rounded-lg overflow-hidden">
        <div className="p-4 border-b border-gray-700">
          <h2 className="font-bold">All Notifications</h2>
        </div>
        {notifications.map(notif => (
          <div key={notif.id} className={`p-4 border-b border-gray-700 hover:bg-gray-750 ${!notif.read ? 'bg-gray-750' : ''}`}>
            <div className="flex items-start gap-4">
              <span className="text-2xl">{getIcon(notif.type)}</span>
              <div className="flex-1">
                <div className="flex justify-between">
                  <h3 className={`font-bold ${getColor(notif.type)}`}>{notif.title}</h3>
                  <span className="text-gray-500 text-sm">{notif.time}</span>
                </div>
                <p className="text-gray-400 text-sm">{notif.message}</p>
              </div>
              {!notif.read && (
                <span className="w-2 h-2 bg-orange-500 rounded-full"></span>
              )}
            </div>
          </div>
        ))}
      </div>

      <div className="mt-6 bg-gray-800 p-4 rounded-lg">
        <h2 className="text-lg font-bold mb-3">⚙️ Notification Settings</h2>
        <div className="space-y-2">
          <label className="flex items-center gap-2">
            <input type="checkbox" defaultChecked />
            <span>Hot leads notifications</span>
          </label>
          <label className="flex items-center gap-2">
            <input type="checkbox" defaultChecked />
            <span>Campaign completed</span>
          </label>
          <label className="flex items-center gap-2">
            <input type="checkbox" defaultChecked />
            <span>Email reply received</span>
          </label>
          <label className="flex items-center gap-2">
            <input type="checkbox" />
            <span>Daily summary</span>
          </label>
        </div>
      </div>
    </div>
  );
}