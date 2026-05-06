import { useState } from 'react';

export default function LandingPage() {
  const [form, setForm] = useState({ name: '', email: '', company: '', message: '' });
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    setSubmitted(true);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-gray-900">
      <div className="container mx-auto px-4 py-8">
        <nav className="flex justify-between items-center mb-12">
          <div className="flex items-center gap-2">
            <span className="text-3xl">🛡️</span>
            <span className="text-2xl font-bold text-white">DMCAShield</span>
          </div>
          <div className="flex gap-4">
            <a href="#features" className="text-gray-300 hover:text-white">Features</a>
            <a href="#pricing" className="text-gray-300 hover:text-white">Pricing</a>
            <a href="#contact" className="text-gray-300 hover:text-white">Contact</a>
          </div>
        </nav>

        <div className="text-center mb-16">
          <h1 className="text-5xl font-bold text-white mb-4">
            Remove Negative Reviews<br/>
            <span className="text-blue-400">Protect Your Reputation</span>
          </h1>
          <p className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
            AI-powered DMCA removal service. We identify, document, and remove 
            fake or malicious reviews from Google, Yelp, and more.
          </p>
          <div className="flex gap-4 justify-center">
            <a href="#contact" className="bg-blue-600 text-white px-8 py-3 rounded-lg font-bold hover:bg-blue-700">
              Get Started
            </a>
            <a href="#demo" className="bg-gray-700 text-white px-8 py-3 rounded-lg hover:bg-gray-600">
              See Demo
            </a>
          </div>
        </div>

        <div id="features" className="grid md:grid-cols-3 gap-6 mb-16">
          <div className="bg-gray-800 p-6 rounded-lg">
            <div className="text-4xl mb-4">🔍</div>
            <h3 className="text-xl font-bold text-white mb-2">AI-Powered Scanning</h3>
            <p className="text-gray-400">Our AI scans 50+ platforms to find all negative reviews about your business.</p>
          </div>
          <div className="bg-gray-800 p-6 rounded-lg">
            <div className="text-4xl mb-4">⚖️</div>
            <h3 className="text-xl font-bold text-white mb-2">DMCA Legal Removal</h3>
            <p className="text-gray-400">We file proper DMCA takedown notices to get reviews removed legally.</p>
          </div>
          <div className="bg-gray-800 p-6 rounded-lg">
            <div className="text-4xl mb-4">📈</div>
            <h3 className="text-xl font-bold text-white mb-2">Real-Time Tracking</h3>
            <p className="text-gray-400">Dashboard shows all your reviews, removal status, and performance.</p>
          </div>
        </div>

        <div id="pricing" className="grid md:grid-cols-3 gap-6 mb-16">
          <div className="bg-gray-800 p-6 rounded-lg border border-gray-700">
            <h3 className="text-xl font-bold text-white mb-2">Starter</h3>
            <p className="text-3xl font-bold text-blue-400 mb-4">$99<span className="text-sm text-gray-400">/mo</span></p>
            <ul className="text-gray-400 space-y-2 mb-6">
              <li>✓ 10 reviews monitored</li>
              <li>✓ 5 DMCA removals/month</li>
              <li>✓ Basic dashboard</li>
              <li>✓ Email support</li>
            </ul>
            <button className="w-full bg-gray-700 text-white py-2 rounded hover:bg-gray-600">Choose Starter</button>
          </div>
          <div className="bg-blue-900 p-6 rounded-lg border-2 border-blue-500">
            <div className="text-sm text-blue-400 mb-2">MOST POPULAR</div>
            <h3 className="text-xl font-bold text-white mb-2">Pro</h3>
            <p className="text-3xl font-bold text-blue-400 mb-4">$249<span className="text-sm text-gray-400">/mo</span></p>
            <ul className="text-gray-300 space-y-2 mb-6">
              <li>✓ 50 reviews monitored</li>
              <li>✓ 20 DMCA removals/month</li>
              <li>✓ Full dashboard</li>
              <li>✓ Priority support</li>
              <li>✓ Monthly reports</li>
            </ul>
            <button className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 font-bold">Choose Pro</button>
          </div>
          <div className="bg-gray-800 p-6 rounded-lg border border-gray-700">
            <h3 className="text-xl font-bold text-white mb-2">Enterprise</h3>
            <p className="text-3xl font-bold text-blue-400 mb-4">$499<span className="text-sm text-gray-400">/mo</span></p>
            <ul className="text-gray-400 space-y-2 mb-6">
              <li>✓ Unlimited reviews</li>
              <li>✓ Unlimited removals</li>
              <li>✓ Custom dashboard</li>
              <li>✓ Dedicated account manager</li>
              <li>✓ API access</li>
            </ul>
            <button className="w-full bg-gray-700 text-white py-2 rounded hover:bg-gray-600">Contact Sales</button>
          </div>
        </div>

        <div id="contact" className="max-w-md mx-auto bg-gray-800 p-8 rounded-lg">
          <h2 className="text-2xl font-bold text-white mb-6 text-center">Get Started Free</h2>
          {submitted ? (
            <div className="text-center text-green-400 py-8">
              <p className="text-xl font-bold">Thank you!</p>
              <p className="text-gray-400">We'll contact you within 24 hours.</p>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-4">
              <input type="text" placeholder="Your Name" value={form.name} onChange={e => setForm({...form, name: e.target.value})}
                className="w-full bg-gray-700 text-white p-3 rounded" required />
              <input type="email" placeholder="Email" value={form.email} onChange={e => setForm({...form, email: e.target.value})}
                className="w-full bg-gray-700 text-white p-3 rounded" required />
              <input type="text" placeholder="Company Name" value={form.company} onChange={e => setForm({...form, company: e.target.value})}
                className="w-full bg-gray-700 text-white p-3 rounded" />
              <textarea placeholder="How can we help?" value={form.message} onChange={e => setForm({...form, message: e.target.value})}
                className="w-full bg-gray-700 text-white p-3 rounded h-24"></textarea>
              <button type="submit" className="w-full bg-blue-600 text-white py-3 rounded font-bold hover:bg-blue-700">
                Request Demo
              </button>
            </form>
          )}
        </div>

        <footer className="text-center text-gray-500 mt-16 py-8">
          <p>© 2026 DMCAShield. All rights reserved.</p>
        </footer>
      </div>
    </div>
  );
}