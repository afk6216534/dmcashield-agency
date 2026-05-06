import { useState } from 'react';

export default function Budget() {
  const [budget, setBudget] = useState({
    monthly_limit: 5000,
    spent: 3247,
    categories: [
      { name: 'Email Tools', allocated: 500, spent: 320 },
      { name: 'AI Services', allocated: 1000, spent: 845 },
      { name: 'Domains', allocated: 200, spent: 150 },
      { name: 'Software', allocated: 300, spent: 280 },
      { name: 'Ads', allocated: 1000, spent: 650 },
      { name: 'Misc', allocated: 500, spent: 402 },
    ]
  });

  const totalSpent = budget.categories.reduce((a, c) => a + c.spent, 0);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">💵 Budget Manager</h1>

      <div className="grid grid-cols-4 gap-4 mb-6">
        <div className="bg-gradient-to-br from-blue-600 to-blue-800 p-6 rounded-xl">
          <p className="text-blue-200 text-sm">Monthly Budget</p>
          <p className="text-3xl font-bold">${budget.monthly_limit.toLocaleString()}</p>
        </div>
        <div className="bg-gradient-to-br from-green-600 to-green-800 p-6 rounded-xl">
          <p className="text-green-200 text-sm">Spent</p>
          <p className="text-3xl font-bold">${totalSpent.toLocaleString()}</p>
        </div>
        <div className="bg-gradient-to-br from-orange-600 to-orange-800 p-6 rounded-xl">
          <p className="text-orange-200 text-sm">Remaining</p>
          <p className="text-3xl font-bold">${(budget.monthly_limit - totalSpent).toLocaleString()}</p>
        </div>
        <div className="bg-gradient-to-br from-purple-600 to-purple-800 p-6 rounded-xl">
          <p className="text-purple-200 text-sm">Usage</p>
          <p className="text-3xl font-bold">{Math.round(totalSpent / budget.monthly_limit * 100)}%</p>
        </div>
      </div>

      <div className="bg-gray-800 rounded-lg overflow-hidden mb-6">
        <table className="w-full">
          <thead className="bg-gray-700">
            <tr>
              <th className="p-3 text-left">Category</th>
              <th className="p-3 text-left">Allocated</th>
              <th className="p-3 text-left">Spent</th>
              <th className="p-3 text-left">Remaining</th>
              <th className="p-3 text-left">Usage</th>
            </tr>
          </thead>
          <tbody>
            {budget.categories.map((cat, i) => (
              <tr key={i} className="border-t border-gray-700">
                <td className="p-3 font-bold">{cat.name}</td>
                <td className="p-3">${cat.allocated}</td>
                <td className="p-3">${cat.spent}</td>
                <td className="p-3 text-green-400">${cat.allocated - cat.spent}</td>
                <td className="p-3">
                  <div className="flex items-center gap-2">
                    <div className="flex-1 bg-gray-700 rounded-full h-2 w-24">
                      <div className="bg-blue-500 h-2 rounded-full" style={{ width: `${(cat.spent / cat.allocated * 100)}%` }}></div>
                    </div>
                    <span>{Math.round(cat.spent / cat.allocated * 100)}%</span>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <button className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
        Edit Budget
      </button>
    </div>
  );
}