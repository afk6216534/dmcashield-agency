import React, { useState, useEffect } from 'react';

export default function Analytics() {
  const [data, setData] = useState({});

  useEffect(() => {
    fetch('/api/analytics')
      .then(r => r.json())
      .then(setData);
  }, []);

  return (
    <div className="analytics">
      <h1>Analytics Dashboard</h1>
      <div className="metrics">
        <div className="metric-card">
          <h3>Total Leads</h3>
          <p className="number">{data.leads?.total || 0}</p>
        </div>
        <div className="metric-card">
          <h3>Hot Leads</h3>
          <p className="number hot">{data.leads?.hot || 0}</p>
        </div>
        <div className="metric-card">
          <h3>Email Open Rate</h3>
          <p className="number">{data.emails?.open_rate || 0}%</p>
        </div>
        <div className="metric-card">
          <h3>Reply Rate</h3>
          <p className="number">{data.emails?.reply_rate || 0}%</p>
        </div>
      </div>
      <div className="charts">
        <div className="chart-card">
          <h3>Funnel Conversion</h3>
          <div className="funnel-viz">
            <div className="funnel-stage" style={{width: '100%'}}>
              <span>Scraped: {data.leads?.total || 0}</span>
            </div>
            <div className="funnel-stage" style={{width: '50%'}}>
              <span>Emailed: {data.leads?.emailed || 0}</span>
            </div>
            <div className="funnel-stage" style={{width: '20%'}}>
              <span>Opened: {data.leads?.opened || 0}</span>
            </div>
            <div className="funnel-stage" style={{width: '10%'}}>
              <span>Hot: {data.leads?.hot || 0}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}