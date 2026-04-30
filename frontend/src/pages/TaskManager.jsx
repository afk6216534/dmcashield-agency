import React, { useState, useEffect } from 'react';

export default function TaskManager() {
  const [tasks, setTasks] = useState([]);

  useEffect(() => {
    fetch('/api/tasks')
      .then(r => r.json())
      .then(setTasks);
  }, []);

  const pauseTask = (id) => {
    fetch(`/api/tasks/${id}/pause`, { method: 'POST' })
      .then(() => fetch('/api/tasks').then(r => r.json()).then(setTasks));
  };

  const resumeTask = (id) => {
    fetch(`/api/tasks/${id}/resume`, { method: 'POST' })
      .then(() => fetch('/api/tasks').then(r => r.json()).then(setTasks));
  };

  return (
    <div className="task-manager">
      <h1>Task Manager</h1>
      <table>
        <thead><tr><th>Task</th><th>Status</th><th>Leads</th><th>Actions</th></tr></thead>
        <tbody>
          {tasks.map(task => (
            <tr key={task.id}>
              <td>{task.business_type} - {task.city}, {task.state}</td>
              <td><span className={`status ${task.status}`}>{task.status}</span></td>
              <td>{task.leads_total} total</td>
              <td>
                {task.status !== 'paused' && task.status !== 'complete' &&
                  <button onClick={() => pauseTask(task.id)}>Pause</button>}
                {task.status === 'paused' &&
                  <button onClick={() => resumeTask(task.id)}>Resume</button>}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}