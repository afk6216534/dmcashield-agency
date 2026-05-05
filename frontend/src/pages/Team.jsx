import { useState, useEffect } from 'react';

const API = import.meta.env.VITE_API_URL || 'https://dmcashield-agency.vercel.app';

export default function Team() {
  const [team, setTeam] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API}/api/team`)
      .then(r => r.json())
      .then(d => { setTeam(d); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  if (loading) return <div className="p-6">Loading...</div>;

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">Team & Departments</h1>

      <div className="grid grid-cols-3 gap-4 mb-6">
        <div className="bg-gray-800 p-4 rounded-lg text-center">
          <p className="text-4xl font-bold text-blue-400">{team?.total_agents || 0}</p>
          <p className="text-gray-400">Total Agents</p>
        </div>
        <div className="bg-gray-800 p-4 rounded-lg text-center">
          <p className="text-4xl font-bold text-green-400">{team?.online || 0}</p>
          <p className="text-gray-400">Online Now</p>
        </div>
        <div className="bg-gray-800 p-4 rounded-lg text-center">
          <p className="text-4xl font-bold text-purple-400">{team?.departments?.length || 0}</p>
          <p className="text-gray-400">Departments</p>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        {team?.departments?.map((dept, i) => (
          <div key={i} className="bg-gray-800 p-4 rounded-lg">
            <div className="flex justify-between items-center mb-2">
              <h3 className="text-lg font-bold">{dept.name}</h3>
              <span className={`px-2 py-1 rounded text-xs ${dept.status === 'active' ? 'bg-green-900 text-green-400' : 'bg-red-900 text-red-400'}`}>
                {dept.status}
              </span>
            </div>
            <div className="grid grid-cols-2 gap-2 text-sm">
              <div className="bg-gray-700 p-2 rounded">
                <p className="text-gray-400">Agents</p>
                <p className="font-bold">{dept.agents}</p>
              </div>
              <div className="bg-gray-700 p-2 rounded">
                <p className="text-gray-400">Tasks Today</p>
                <p className="font-bold">{dept.tasks_today}</p>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="mt-6 bg-gray-800 p-4 rounded-lg">
        <h2 className="text-lg font-bold mb-3">🤖 AI Agent System</h2>
        <p className="text-gray-400">
          The agency runs on autonomous AI agents organized into departments. 
          Each department handles specific tasks: Scraping, Validation, Marketing, Sales, and DMCA.
        </p>
      </div>
    </div>
  );
}