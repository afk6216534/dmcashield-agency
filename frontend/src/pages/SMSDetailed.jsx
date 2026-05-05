import { useState } from 'react';

export default function SMSDetailed() {
  const [message, setMessage] = useState('');
  const [contacts, setContacts] = useState([
    { id: 1, name: 'John Doe', phone: '+1234567890', status: 'active' },
    { id: 2, name: 'Jane Smith', phone: '+1234567891', status: 'active' },
    { id: 3, name: 'Bob Wilson', phone: '+1234567892', status: 'inactive' },
  ]);
  const [sending, setSending] = useState(false);

  const sendSMS = () => {
    if (!message) return;
    setSending(true);
    setTimeout(() => {
      setSending(false);
      setMessage('');
      alert('SMS sent to ' + contacts.filter(c => c.status === 'active').length + ' contacts');
    }, 1500);
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">💬 SMS Campaign Manager</h1>

      <div className="grid grid-cols-4 gap-4 mb-6">
        <div className="bg-gradient-to-br from-blue-600 to-blue-800 p-6 rounded-xl">
          <p className="text-blue-200 text-sm">Active Contacts</p>
          <p className="text-3xl font-bold">{contacts.filter(c => c.status === 'active').length}</p>
        </div>
        <div className="bg-gradient-to-br from-green-600 to-green-800 p-6 rounded-xl">
          <p className="text-green-200 text-sm">Sent Today</p>
          <p className="text-3xl font-bold">12</p>
        </div>
        <div className="bg-gradient-to-br from-purple-600 to-purple-800 p-6 rounded-xl">
          <p className="text-purple-200 text-sm">Delivered</p>
          <p className="text-3xl font-bold">11</p>
        </div>
        <div className="bg-gradient-to-br from-orange-600 to-orange-800 p-6 rounded-xl">
          <p className="text-orange-200 text-sm">Credit Balance</p>
          <p className="text-3xl font-bold">488</p>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-6">
        <div className="bg-gray-800 p-4 rounded-lg">
          <h2 className="text-lg font-bold mb-4">📝 Send SMS</h2>
          <div className="space-y-4">
            <div>
              <label className="block text-gray-400 mb-2">Recipients</label>
              <div className="bg-gray-700 p-3 rounded">
                <p className="text-sm">{contacts.filter(c => c.status === 'active').length} active contacts selected</p>
              </div>
            </div>
            <div>
              <label className="block text-gray-400 mb-2">Message</label>
              <textarea value={message} onChange={e => setMessage(e.target.value)}
                className="w-full bg-gray-700 text-white p-3 rounded h-32" placeholder="Type your message..." />
              <p className="text-gray-500 text-sm mt-1">{message.length}/160 characters</p>
            </div>
            <button onClick={sendSMS} disabled={sending || !message}
              className="w-full bg-blue-600 text-white py-3 rounded-lg font-bold hover:bg-blue-700 disabled:opacity-50">
              {sending ? 'Sending...' : '📤 Send SMS'}
            </button>
          </div>
        </div>

        <div className="bg-gray-800 p-4 rounded-lg">
          <h2 className="text-lg font-bold mb-4">👥 Contacts</h2>
          <div className="space-y-2">
            {contacts.map(contact => (
              <div key={contact.id} className="bg-gray-700 p-3 rounded flex justify-between items-center">
                <div>
                  <p className="font-bold">{contact.name}</p>
                  <p className="text-gray-400 text-sm">{contact.phone}</p>
                </div>
                <span className={`px-2 py-1 rounded text-xs ${contact.status === 'active' ? 'bg-green-900 text-green-400' : 'bg-gray-600'}`}>
                  {contact.status}
                </span>
              </div>
            ))}
          </div>
          <button className="mt-4 w-full bg-gray-700 py-2 rounded text-sm hover:bg-gray-600">+ Add Contact</button>
        </div>
      </div>

      <div className="mt-6 bg-gray-800 p-4 rounded-lg">
        <h2 className="text-lg font-bold mb-3">📊 Recent Messages</h2>
        <div className="space-y-2">
          <div className="bg-gray-700 p-3 rounded">
            <div className="flex justify-between">
              <span className="font-bold">Campaign Update</span>
              <span className="text-green-400">Delivered</span>
            </div>
            <p className="text-gray-400 text-sm">Sent to 3 contacts • 2 min ago</p>
          </div>
          <div className="bg-gray-700 p-3 rounded">
            <div className="flex justify-between">
              <span className="font-bold">Follow up</span>
              <span className="text-green-400">Delivered</span>
            </div>
            <p className="text-gray-400 text-sm">Sent to 5 contacts • 1 hour ago</p>
          </div>
        </div>
      </div>
    </div>
  );
}