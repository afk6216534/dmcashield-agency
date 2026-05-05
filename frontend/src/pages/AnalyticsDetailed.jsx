import { useState, useEffect } from 'react';

const API = import.meta.env.VITE_API_URL || 'https://dmcashield-agency.vercel.app';

export default function AnalyticsDetailed() {
  const [analytics, setAnalytics] = useState(null);
  const [subjects, setSubjects] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      fetch(`${API}/api/analytics`).then(r => r.json()),
      fetch(`${API}/api/analytics/top-subjects`).then(r => r.json())
    ]).then(([a, s]) => {
      setAnalytics(a);
      setSubjects(s);
      setLoading(false);
    }).catch(() => setLoading(false));
  }, []);

  if (loading) return <div className="p-6">Loading...</div>;

  const openRate = analytics?.open_rate || 0;
  const replyRate = analytics?.reply_rate || 0;

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">📈 Advanced Analytics</h1>

      <div className="grid grid-cols-4 gap-4 mb-6">
        <div className="bg-gradient-to-br from-blue-600 to-blue-800 p-6 rounded-xl">
          <p className="text-blue-200 text-sm">Total Leads</p>
          <p className="text-3xl font-bold">{analytics?.total_leads}</p>
        </div>
        <div className="bg-gradient-to-br from-green-600 to-green-800 p-6 rounded-xl">
          <p className="text-green-200 text-sm">Emails Sent</p>
          <p className="text-3xl font-bold">{analytics?.total_emails_sent}</p>
        </div>
        <div className="bg-gradient-to-br from-purple-600 to-purple-800 p-6 rounded-xl">
          <p className="text-purple-200 text-sm">Open Rate</p>
          <p className="text-3xl font-bold">{openRate}%</p>
          <div className="w-full bg-black/20 h-2 rounded-full mt-2">
            <div className="bg-white h-2 rounded-full" style={{ width: `${openRate}%` }}></div>
          </div>
        </div>
        <div className="bg-gradient-to-br from-orange-600 to-orange-800 p-6 rounded-xl">
          <p className="text-orange-200 text-sm">Reply Rate</p>
          <p className="text-3xl font-bold">{replyRate}%</p>
          <div className="w-full bg-black/20 h-2 rounded-full mt-2">
            <div className="bg-white h-2 rounded-full" style={{ width: `${replyRate * 5}%` }}></div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-6 mb-6">
        <div className="bg-gray-800 p-4 rounded-lg">
          <h2 className="text-lg font-bold mb-4">🔥 Hot Leads</h2>
          <div className="text-center p-8">
            <p className="text-5xl font-bold text-orange-400">{analytics?.hot_leads}</p>
            <p className="text-gray-400 mt-2">Ready for conversion</p>
          </div>
        </div>
        <div className="bg-gray-800 p-4 rounded-lg">
          <h2 className="text-lg font-bold mb-4">💰 Converted</h2>
          <div className="text-center p-8">
            <p className="text-5xl font-bold text-green-400">{analytics?.converted}</p>
            <p className="text-gray-400 mt-2">Clients acquired</p>
          </div>
        </div>
      </div>

      <div className="bg-gray-800 p-4 rounded-lg mb-6">
        <h2 className="text-lg font-bold mb-4">📧 Top Performing Subjects</h2>
        <div className="space-y-3">
          {subjects.map((sub, i) => {
            const rate = ((sub.opens / sub.sends) * 100).toFixed(1);
            return (
              <div key={i} className="flex items-center gap-4">
                <span className="text-gray-400 w-8">#{i + 1}</span>
                <span className="flex-1 truncate">{sub.subject}</span>
                <div className="w-32 bg-gray-700 rounded-full h-2">
                  <div className="bg-blue-500 h-2 rounded-full" style={{ width: `${rate}%` }}></div>
                </div>
                <span className="text-right w-16">{rate}%</span>
                <span className="text-gray-500 text-sm w-12">{sub.sends} sent</span>
              </div>
            );
          })}
        </div>
      </div>

      <div className="grid grid-cols-3 gap-4">
        <div className="bg-gray-800 p-4 rounded-lg text-center">
          <p className="text-gray-400 text-sm">Opened</p>
          <p className="text-2xl font-bold text-blue-400">{analytics?.total_opened}</p>
        </div>
        <div className="bg-gray-800 p-4 rounded-lg text-center">
          <p className="text-gray-400 text-sm">Replied</p>
          <p className="text-2xl font-bold text-green-400">{analytics?.total_replied}</p>
        </div>
        <div className="bg-gray-800 p-4 rounded-lg text-center">
          <p className="text-gray-400 text-sm">Conversion</p>
          <p className="text-2xl font-bold text-purple-400">
            {analytics?.total_leads ? ((analytics.converted / analytics.total_leads) * 100).toFixed(1) : 0}%
          </p>
        </div>
      </div>
    </div>
  );
}