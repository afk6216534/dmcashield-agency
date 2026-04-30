import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Users, Mail, MessageSquare, TrendingUp, Play, Flame, ArrowRight } from 'lucide-react';

export default function Dashboard() {
  const [stats, setStats] = useState({});

  useEffect(() => {
    fetch('/api/status')
      .then(r => r.json())
      .then(setStats);
  }, []);

  return (
    <div style={{ padding: '24px' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '32px' }}>
        <div>
          <h1 style={{ fontSize: '32px', fontWeight: 'bold', marginBottom: '8px' }}>DMCAShield Command Center</h1>
          <p style={{ color: '#8b949e' }}>Welcome back. Here's your agency overview.</p>
        </div>
        <Link to="/launch-task" style={{ 
          background: 'linear-gradient(135deg, #6C63FF, #4f46e5)', 
          color: 'white', padding: '12px 24px', borderRadius: '10px', 
          fontWeight: '600', textDecoration: 'none', display: 'flex', alignItems: 'center', gap: '8px'
        }}>
          <Play size={16} /> Launch Campaign
        </Link>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '20px', marginBottom: '32px' }}>
        {[
          { label: 'Active Leads', value: stats.stats?.hot_leads || 0, icon: Users, color: '#6C63FF' },
          { label: 'Open Rate', value: stats.stats?.open_rate || 0, icon: Mail, color: '#22d3ee', isPercent: true },
          { label: 'Reply Rate', value: stats.stats?.reply_rate || 0, icon: MessageSquare, color: '#10b981', isPercent: true },
          { label: 'Conversion', value: stats.stats?.conversion_rate || 0, icon: TrendingUp, color: '#f97316', isPercent: true },
        ].map((stat, i) => (
          <div key={i} style={{
            background: 'linear-gradient(135deg, rgba(22,27,34,0.9), rgba(28,35,51,0.7))',
            backdropFilter: 'blur(16px)', border: '1px solid rgba(48,54,61,0.5)',
            borderRadius: '16px', padding: '24px'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '16px' }}>
              <div style={{ width: '48px', height: '48px', borderRadius: '12px', 
                background: `${stat.color}20`, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <stat.icon size={24} color={stat.color} />
              </div>
              <span style={{ fontSize: '12px', fontWeight: '600', color: '#10b981' }}>+12%</span>
            </div>
            <p style={{ fontSize: '32px', fontWeight: 'bold', marginBottom: '4px' }}>
              {stat.value}{stat.isPercent ? '%' : ''}
            </p>
            <p style={{ fontSize: '14px', color: '#8b949e' }}>{stat.label}</p>
          </div>
        ))}
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '20px' }}>
        <div style={{
          background: 'linear-gradient(135deg, rgba(22,27,34,0.9), rgba(28,35,51,0.7))',
          backdropFilter: 'blur(16px)', border: '1px solid rgba(48,54,61,0.5)',
          borderRadius: '16px', padding: '24px'
        }}>
          <h2 style={{ fontSize: '20px', fontWeight: '600', marginBottom: '20px' }}>Recent Activity</h2>
          {[
            { task: 'Dental Clinics LA', status: 'active', leads: 234 },
            { task: 'Pizza Shops NYC', status: 'complete', leads: 156 },
            { task: 'Law Firms TX', status: 'paused', leads: 89 },
          ].map((task, i) => (
            <div key={i} style={{ 
              display: 'flex', justifyContent: 'space-between', alignItems: 'center', 
              padding: '16px', background: 'rgba(33,38,45,0.5)', borderRadius: '12px', marginBottom: '12px'
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                <Flame size={20} color="#f97316" />
                <div>
                  <p style={{ fontWeight: '600' }}>{task.task}</p>
                  <p style={{ fontSize: '14px', color: '#8b949e' }}>{task.leads} leads</p>
                </div>
              </div>
              <span style={{ 
                padding: '4px 12px', borderRadius: '100px', fontSize: '12px', fontWeight: '600',
                background: task.status === 'active' ? 'rgba(16,185,129,0.15)' : task.status === 'complete' ? 'rgba(108,99,255,0.15)' : 'rgba(139,148,158,0.15)',
                color: task.status === 'active' ? '#6ee7b7' : task.status === 'complete' ? '#c4b5fd' : '#8b949e'
              }}>{task.status}</span>
            </div>
          ))}
        </div>

        <div style={{
          background: 'linear-gradient(135deg, rgba(22,27,34,0.9), rgba(28,35,51,0.7))',
          backdropFilter: 'blur(16px)', border: '1px solid rgba(48,54,61,0.5)',
          borderRadius: '16px', padding: '24px'
        }}>
          <h2 style={{ fontSize: '20px', fontWeight: '600', marginBottom: '20px' }}>Quick Actions</h2>
          {[
            { label: 'Browse Leads', icon: Users, color: '#6C63FF', path: '/leads' },
            { label: 'New Campaign', icon: Play, color: '#22d3ee', path: '/launch-task' },
            { label: 'Hot Leads', icon: Flame, color: '#f43f5e', path: '/hot-leads' },
            { label: 'Analytics', icon: TrendingUp, color: '#10b981', path: '/analytics' },
          ].map((action, i) => (
            <Link key={i} to={action.path} style={{ 
              display: 'flex', alignItems: 'center', gap: '12px', padding: '16px', 
              background: 'rgba(33,38,45,0.5)', borderRadius: '12px', marginBottom: '12px',
              textDecoration: 'none', color: 'inherit'
            }}>
              <action.icon size={20} color={action.color} />
              <span>{action.label}</span>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}