import { NavLink, useLocation } from 'react-router-dom';

const navItems = [
  { to: '/', icon: '📊', label: 'Dashboard', section: 'command' },
  { to: '/system', icon: '🏢', label: 'Control Tower', section: 'command' },
  { to: '/launch', icon: '🚀', label: 'Launch Task', section: 'command' },
  { to: '/leads', icon: '👥', label: 'Lead Database', section: 'operations' },
  { to: '/accounts', icon: '📧', label: 'Email Accounts', section: 'operations' },
  { to: '/campaigns', icon: '📣', label: 'Campaigns', section: 'operations' },
  { to: '/warmup', icon: '🔥', label: 'Email Warmup', section: 'operations' },
  { to: '/analytics', icon: '📈', label: 'Analytics', section: 'intelligence' },
  { to: '/tasks', icon: '📋', label: 'Task Manager', section: 'intelligence' },
  { to: '/hot-leads', icon: '🔥', label: 'Hot Leads', section: 'intelligence' },
  { to: '/sms', icon: '💬', label: 'SMS Campaign', section: 'channels' },
  { to: '/whatsapp', icon: '📱', label: 'WhatsApp', section: 'channels' },
  { to: '/linkedin', icon: '💼', label: 'LinkedIn', section: 'channels' },
  { to: '/cold-call', icon: '📞', label: 'Cold Call', section: 'channels' },
  { to: '/schedule', icon: '📅', label: 'Scheduler', section: 'automation' },
  { to: '/ai-responses', icon: '🤖', label: 'AI Response', section: 'automation' },
  { to: '/integrations', icon: '🔗', label: 'Integrations', section: 'automation' },
  { to: '/learning', icon: '🧠', label: 'Self-Learning', section: 'automation' },
  { to: '/settings', icon: '⚙️', label: 'Settings', section: 'system' },
];

const sections = {
  command: 'Command Center',
  operations: 'Operations',
  intelligence: 'Intelligence',
  channels: 'Channels',
  automation: 'Automation',
  system: 'System',
};

export default function Sidebar({ systemStatus, hotLeadCount }) {
  const location = useLocation();

  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <div className="logo-icon">🛡️</div>
        <div>
          <h1>DMCAShield</h1>
          <div className="version">Control Tower v2.0</div>
        </div>
      </div>

      <nav className="sidebar-nav">
        {Object.entries(sections).map(([key, label]) => (
          <div key={key}>
            <div className="nav-section-label">{label}</div>
            {navItems
              .filter((item) => item.section === key)
              .map((item) => (
                <NavLink
                  key={item.to}
                  to={item.to}
                  className={({ isActive }) =>
                    `nav-item ${isActive ? 'active' : ''}`
                  }
                >
                  <span className="nav-icon">{item.icon}</span>
                  <span>{item.label}</span>
                  {item.to === '/hot-leads' && hotLeadCount > 0 && (
                    <span className="nav-badge">{hotLeadCount}</span>
                  )}
                </NavLink>
              ))}
          </div>
        ))}
      </nav>

      <div className="sidebar-status">
        <span className={`status-dot ${systemStatus === 'operational' ? 'green' : systemStatus === 'degraded' ? 'yellow' : 'red'}`}></span>
        <span style={{ fontSize: '0.78rem', color: 'var(--text-secondary)' }}>
          {systemStatus === 'operational' ? '12 depts • 36 agents' : systemStatus || 'connecting...'}
        </span>
      </div>
    </aside>
  );
}
