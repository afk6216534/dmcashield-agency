import { useState } from 'react';

export default function WhatsAppDetailed() {
  const [template, setTemplate] = useState('');
  const [sending, setSending] = useState(false);

  const templates = [
    { id: 1, name: 'Initial Contact', usage: 45 },
    { id: 2, name: 'Follow Up', usage: 32 },
    { id: 3, name: 'Meeting Request', usage: 18 },
  ];

  const sendMessage = () => {
    setSending(true);
    setTimeout(() => {
      setSending(false);
      alert('WhatsApp message sent!');
    }, 1500);
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">📱 WhatsApp Business</h1>

      <div className="grid grid-cols-4 gap-4 mb-6">
        <div className="bg-gradient-to-br from-green-600 to-green-800 p-6 rounded-xl">
          <p className="text-green-200 text-sm">Messages Today</p>
          <p className="text-3xl font-bold">28</p>
        </div>
        <div className="bg-gradient-to-br from-blue-600 to-blue-800 p-6 rounded-xl">
          <p className="text-blue-200 text-sm">Delivered</p>
          <p className="text-3xl font-bold">26</p>
        </div>
        <div className="bg-gradient-to-br from-purple-600 to-purple-800 p-6 rounded-xl">
          <p className="text-purple-200 text-sm">Read</p>
          <p className="text-3xl font-bold">22</p>
        </div>
        <div className="bg-gradient-to-br from-orange-600 to-orange-800 p-6 rounded-xl">
          <p className="text-orange-200 text-sm">Replies</p>
          <p className="text-3xl font-bold">8</p>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-6">
        <div className="bg-gray-800 p-4 rounded-lg">
          <h2 className="text-lg font-bold mb-4">📝 Send Message</h2>
          <div className="space-y-4">
            <div>
              <label className="block text-gray-400 mb-2">Template</label>
              <select value={template} onChange={e => setTemplate(e.target.value)}
                className="w-full bg-gray-700 text-white p-2 rounded">
                <option value="">Select template...</option>
                {templates.map(t => <option key={t.id} value={t.id}>{t.name}</option>)}
              </select>
            </div>
            <div>
              <label className="block text-gray-400 mb-2">Recipients</label>
              <input placeholder="Enter phone numbers (comma separated)" 
                className="w-full bg-gray-700 text-white p-2 rounded" />
            </div>
            <button onClick={sendMessage} disabled={sending}
              className="w-full bg-green-600 text-white py-3 rounded-lg font-bold disabled:opacity-50">
              {sending ? 'Sending...' : '📤 Send via WhatsApp'}
            </button>
          </div>
        </div>

        <div className="bg-gray-800 p-4 rounded-lg">
          <h2 className="text-lg font-bold mb-4">📋 Templates</h2>
          <div className="space-y-2">
            {templates.map(t => (
              <div key={t.id} className="bg-gray-700 p-3 rounded flex justify-between">
                <span className="font-bold">{t.name}</span>
                <span className="text-gray-400">{t.usage} uses</span>
              </div>
            ))}
          </div>
          <button className="mt-4 w-full bg-gray-700 py-2 rounded text-sm hover:bg-gray-600">+ New Template</button>
        </div>
      </div>
    </div>
  );
}