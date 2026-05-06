import { useState } from 'react';

export default function Goals() {
  const [goals, setGoals] = useState([
    { id: 1, title: 'Get 50 new clients', progress: 72, target: 50, current: 36, timeframe: 'Q2 2026' },
    { id: 2, title: '$50K monthly revenue', progress: 65, target: 50000, current: 32500, timeframe: 'Q2 2026' },
    { id: 3, title: 'Remove 100 reviews', progress: 45, target: 100, current: 45, timeframe: 'Q2 2026' },
    { id: 4, title: 'Launch mobile app', progress: 20, target: 100, current: 20, timeframe: 'Q3 2026' },
  ]);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">🎯 Goals & Targets</h1>

      <div className="grid grid-cols-4 gap-4 mb-6">
        <div className="bg-gray-800 p-4 rounded-lg text-center">
          <p className="text-gray-400 text-sm">Total Goals</p>
          <p className="text-2xl font-bold">{goals.length}</p>
        </div>
        <div className="bg-gray-800 p-4 rounded-lg text-center">
          <p className="text-gray-400 text-sm">On Track</p>
          <p className="text-2xl font-bold text-green-400">{goals.filter(g => g.progress >= 50).length}</p>
        </div>
        <div className="bg-gray-800 p-4 rounded-lg text-center">
          <p className="text-gray-400 text-sm">At Risk</p>
          <p className="text-2xl font-bold text-yellow-400">{goals.filter(g => g.progress >= 30 && g.progress < 50).length}</p>
        </div>
        <div className="bg-gray-800 p-4 rounded-lg text-center">
          <p className="text-gray-400 text-sm">Behind</p>
          <p className="text-2xl font-bold text-red-400">{goals.filter(g => g.progress < 30).length}</p>
        </div>
      </div>

      <div className="space-y-4">
        {goals.map(goal => (
          <div key={goal.id} className="bg-gray-800 p-4 rounded-lg">
            <div className="flex justify-between items-start mb-3">
              <div>
                <h3 className="font-bold text-lg">{goal.title}</h3>
                <p className="text-gray-400 text-sm">{goal.timeframe}</p>
              </div>
              <span className={`px-3 py-1 rounded text-sm ${goal.progress >= 50 ? 'bg-green-900 text-green-400' : goal.progress >= 30 ? 'bg-yellow-900 text-yellow-400' : 'bg-red-900 text-red-400'}`}>
                {goal.progress >= 50 ? 'On Track' : goal.progress >= 30 ? 'At Risk' : 'Behind'}
              </span>
            </div>
            <div className="flex items-center gap-4">
              <div className="flex-1 bg-gray-700 rounded-full h-3">
                <div className={`h-3 rounded-full ${goal.progress >= 50 ? 'bg-green-500' : goal.progress >= 30 ? 'bg-yellow-500' : 'bg-red-500'}`} style={{ width: `${goal.progress}%` }}></div>
              </div>
              <span className="text-right w-32">
                {goal.current.toLocaleString()} / {goal.target.toLocaleString()}
              </span>
            </div>
            <p className="text-gray-400 text-sm mt-2">{goal.progress}% complete</p>
          </div>
        ))}
      </div>

      <button className="mt-6 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
        + Add Goal
      </button>
    </div>
  );
}