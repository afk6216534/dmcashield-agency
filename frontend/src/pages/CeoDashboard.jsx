import React, { useState, useEffect } from 'react';

export default function CeoDashboard() {
  const [status, setStatus] = useState({});
  const [soul, setSoul] = useState({});
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [statusRes, soulRes] = await Promise.all([
          fetch('/api/status').then(r => r.json()),
          fetch('/api/soul').then(r => r.json())
        ]);
        setStatus(statusRes);
        setSoul(soulRes);
      } catch (err) {
        console.error('Failed to fetch CEO dashboard data:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 30000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return <div className="ceo-dashboard">Loading CEO overview...</div>;
  }

  const depts = status.departments_status || {};
  const deptList = Object.entries(depts).map(([name, status]) => (
    <div key={name} className="dept-status">
      <span className="dept-name">{name}</span>:
      <span className={`status ${status === 'online' ? 'online' : 'offline'}`}>
        {status}
      </span>
    </div>
  ));

  return (
    <div className="ceo-dashboard">
      <h1>👔 CEO Dashboard - DMCAShield Agency</h1>
      <div className="ceo-grid">
        <div className="ceo-card">
          <h2>System Status</h2>
          <p><strong>Status:</strong> {status.system?.status || 'unknown'}</p>
          <p><strong>Version:</strong> {status.system?.version || 'N/A'}</p>
          <p><strong>Uptime:</strong> {status.system?.total_autonomous_hours || 0} hours</p>
          <p><strong>Learning Cycle:</strong> {status.system?.learning_cycle || 0}</p>
        </div>
        <div className="ceo-card">
          <h2>Department Status</h2>
          {deptList}
        </div>
        <div className="ceo-card">
          <h2>Soul Snapshot</h2>
          <p><strong>Mission:</strong> {soul.mission || 'N/A'}</p>
          <p><strong>Principles:</strong> {soul.core_principles?.length || 0} principles</p>
          <p><strong>Departments:</strong> {Object.keys(soul.departments || {}).length} tracked</p>
          <p><strong>Last Update:</strong> {new Date(soul.creation_date || 0).toLocaleString()}</p>
        </div>
        <div className="ceo-card">
          <h2>Quick Actions</h2>
          <button onClick={() => window.open('/api/docs', '_blank')}>
            View API Docs
          </button>
          <button onClick={() => window.open('/', '_blank')}>
            Return to Main Dashboard
          </button>
        </div>
      </div>
    </div>
  );
}