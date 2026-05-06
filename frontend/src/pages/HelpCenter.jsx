import { useState } from 'react';

export default function HelpCenter() {
  const [category, setCategory] = useState('getting-started');

  const categories = [
    { id: 'getting-started', label: 'Getting Started', icon: '🚀' },
    { id: 'leads', label: 'Lead Management', icon: '👥' },
    { id: 'email', label: 'Email Campaigns', icon: '📧' },
    { id: 'automation', label: 'Automation', icon: '⚡' },
    { id: 'api', label: 'API Docs', icon: '🔌' },
  ];

  const articles = {
    'getting-started': [
      { q: 'How do I launch my first campaign?', a: 'Go to Quick Launch, enter business type, city, and state. Click Launch Campaign to start.' },
      { q: 'What is lead scoring?', a: 'Lead scoring rates leads 0-100 based on review count, business info, and contact quality. Hot leads score 80+.' },
      { q: 'How does email warmup work?', a: 'Warmup gradually increases emails from 5 to 40/day over 28 days to build sender reputation.' },
    ],
    'leads': [
      { q: 'Where do leads come from?', a: 'Leads are scraped from Google Maps, Hunter.io, and Apollo.io based on your campaign criteria.' },
      { q: 'How do I filter hot leads?', a: 'Use Lead Scoring page to filter leads by temperature (hot/warm/cold) and score.' },
    ],
    'email': [
      { q: 'How many emails can I send per day?', a: 'Default limit is 40 emails/day per account. Increase as accounts complete warmup.' },
      { q: 'What is the email funnel?', a: '6-email sequence: intro, social proof, fear trigger, value offer, last chance, breakup.' },
    ],
    'automation': [
      { q: 'How does JARVIS work?', a: 'JARVIS is your AI assistant. Ask questions like "how many leads" or "show system status".' },
      { q: 'Can I schedule campaigns?', a: 'Use Scheduler page to schedule when campaigns send emails.' },
    ],
    'api': [
      { q: 'What APIs are available?', a: 'GET /api/leads, /api/tasks, /api/campaigns, /api/clients, /api/revenue, /api/team, /api/dmca/cases' },
      { q: 'How do I connect via API?', a: 'Use https://dmcashield-agency.vercel.app as base URL with any API client.' },
    ],
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">❓ Help Center</h1>

      <div className="grid grid-cols-5 gap-4 mb-6">
        {categories.map(cat => (
          <button key={cat.id} onClick={() => setCategory(cat.id)}
            className={`p-4 rounded-lg text-center ${category === cat.id ? 'bg-blue-600' : 'bg-gray-800 hover:bg-gray-700'}`}>
            <span className="text-2xl block mb-1">{cat.icon}</span>
            <span className="text-sm">{cat.label}</span>
          </button>
        ))}
      </div>

      <div className="bg-gray-800 p-4 rounded-lg">
        <h2 className="text-lg font-bold mb-4">{categories.find(c => c.id === category)?.label}</h2>
        <div className="space-y-4">
          {articles[category]?.map((article, i) => (
            <div key={i} className="bg-gray-700 p-4 rounded">
              <h3 className="font-bold mb-2">Q: {article.q}</h3>
              <p className="text-gray-400">A: {article.a}</p>
            </div>
          ))}
        </div>
      </div>

      <div className="mt-6 bg-gray-800 p-4 rounded-lg">
        <h2 className="text-lg font-bold mb-3">💬 Need More Help?</h2>
        <p className="text-gray-400 mb-3">Ask JARVIS AI for instant answers!</p>
        <a href="#/ai-detailed" className="bg-blue-600 px-4 py-2 rounded inline-block">Chat with JARVIS</a>
      </div>
    </div>
  );
}