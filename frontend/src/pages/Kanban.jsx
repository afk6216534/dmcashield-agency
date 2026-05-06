import { useState } from 'react';

const initialTasks = [
  { id: 1, title: 'Setup campaign for dentist LA', status: 'todo', priority: 'high' },
  { id: 2, title: 'Review lead scoring algorithm', status: 'in_progress', priority: 'medium' },
  { id: 3, title: 'Fix warmup delay on account 2', status: 'done', priority: 'low' },
  { id: 4, title: 'Add new email templates', status: 'todo', priority: 'medium' },
  { id: 5, title: 'Update integration with Twilio', status: 'in_progress', priority: 'high' },
];

export default function Kanban() {
  const [tasks, setTasks] = useState(initialTasks);
  const [showAdd, setShowAdd] = useState(false);
  const [newTask, setNewTask] = useState('');

  const columns = [
    { id: 'todo', label: 'To Do', color: '#6b7280' },
    { id: 'in_progress', label: 'In Progress', color: '#3b82f6' },
    { id: 'done', label: 'Done', color: '#10b981' },
  ];

  const addTask = () => {
    if (!newTask) return;
    setTasks([...tasks, { id: Date.now(), title: newTask, status: 'todo', priority: 'medium' }]);
    setNewTask('');
    setShowAdd(false);
  };

  const moveTask = (taskId, direction) => {
    setTasks(tasks.map(t => {
      if (t.id !== taskId) return t;
      const idx = columns.findIndex(c => c.id === t.status);
      if (direction === 'next' && idx < columns.length - 1) {
        return { ...t, status: columns[idx + 1].id };
      } else if (direction === 'prev' && idx > 0) {
        return { ...t, status: columns[idx - 1].id };
      }
      return t;
    }));
  };

  const getPriorityColor = (priority) => {
    if (priority === 'high') return 'text-red-400';
    if (priority === 'medium') return 'text-yellow-400';
    return 'text-green-400';
  };

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">📋 Task Kanban</h1>
        <button onClick={() => setShowAdd(true)} className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
          + Add Task
        </button>
      </div>

      {showAdd && (
        <div className="bg-gray-800 p-4 rounded-lg mb-4">
          <input value={newTask} onChange={e => setNewTask(e.target.value)}
            className="w-full bg-gray-700 text-white p-2 rounded mb-2" placeholder="Task title..." autoFocus />
          <div className="flex gap-2">
            <button onClick={addTask} className="bg-green-600 px-4 py-2 rounded">Add</button>
            <button onClick={() => setShowAdd(false)} className="bg-gray-600 px-4 py-2 rounded">Cancel</button>
          </div>
        </div>
      )}

      <div className="grid grid-cols-3 gap-4">
        {columns.map((col, idx) => (
          <div key={col.id} className="bg-gray-800 rounded-lg">
            <div className="p-3 border-b border-gray-700" style={{ borderTop: `3px solid ${col.color}` }}>
              <h3 className="font-bold">{col.label}</h3>
              <p className="text-gray-400 text-sm">{tasks.filter(t => t.status === col.id).length} tasks</p>
            </div>
            <div className="p-2 space-y-2 min-h-64">
              {tasks.filter(t => t.status === col.id).map(task => (
                <div key={task.id} className="bg-gray-700 p-3 rounded">
                  <div className="flex justify-between items-start mb-2">
                    <p className="font-bold text-sm">{task.title}</p>
                    <span className={`text-xs ${getPriorityColor(task.priority)}`}>● {task.priority}</span>
                  </div>
                  <div className="flex gap-2">
                    {idx > 0 && (
                      <button onClick={() => moveTask(task.id, 'prev')} className="text-gray-400 hover:text-white text-sm">←</button>
                    )}
                    {idx < columns.length - 1 && (
                      <button onClick={() => moveTask(task.id, 'next')} className="text-gray-400 hover:text-white text-sm">→</button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}