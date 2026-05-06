import { NavLink, useLocation } from 'react-router-dom';

const navItems = [
  { to: '/', icon: '📊', label: 'Dashboard', section: 'command' },
  { to: '/overview', icon: '📋', label: 'Overview', section: 'command' },
  { to: '/command-center', icon: '🎛️', label: 'Command Center', section: 'command' },
  { to: '/system', icon: '🏢', label: 'Control Tower', section: 'command' },
  { to: '/system-health', icon: '💹', label: 'System Health', section: 'command' },
  { to: '/launch', icon: '🚀', label: 'Launch Task', section: 'command' },
  { to: '/quick-launch', icon: '⚡', label: 'Quick Launch', section: 'command' },
  { to: '/leads', icon: '👥', label: 'Lead Database', section: 'operations' },
  { to: '/leads-detailed', icon: '🔍', label: 'Lead Details', section: 'operations' },
  { to: '/accounts', icon: '📧', label: 'Email Accounts', section: 'operations' },
  { to: '/email-detailed', icon: '📬', label: 'Email Manager', section: 'operations' },
  { to: '/campaigns', icon: '📣', label: 'Campaigns', section: 'operations' },
  { to: '/campaign-performance', icon: '📊', label: 'Campaign Performance', section: 'operations' },
  { to: '/templates', icon: '📝', label: 'Templates', section: 'operations' },
  { to: '/warmup', icon: '🔥', label: 'Email Warmup', section: 'operations' },
  { to: '/warmup-detailed', icon: '🌡️', label: 'Warmup System', section: 'operations' },
  { to: '/analytics', icon: '📈', label: 'Analytics', section: 'intelligence' },
  { to: '/analytics-advanced', icon: '📊', label: 'Advanced Analytics', section: 'intelligence' },
  { to: '/lead-scoring', icon: '🎯', label: 'Lead Scoring', section: 'intelligence' },
  { to: '/tasks', icon: '📋', label: 'Task Manager', section: 'intelligence' },
  { to: '/tasks-detailed', icon: '✅', label: 'Task Details', section: 'intelligence' },
  { to: '/hot-leads', icon: '🔥', label: 'Hot Leads', section: 'intelligence' },
  { to: '/reports', icon: '📑', label: 'Reports', section: 'intelligence' },
  { to: '/sms', icon: '💬', label: 'SMS Campaign', section: 'channels' },
  { to: '/sms-detailed', icon: '📱', label: 'SMS Manager', section: 'channels' },
  { to: '/whatsapp', icon: '📱', label: 'WhatsApp', section: 'channels' },
  { to: '/whatsapp-detailed', icon: '💬', label: 'WhatsApp Manager', section: 'channels' },
  { to: '/linkedin', icon: '💼', label: 'LinkedIn', section: 'channels' },
  { to: '/linkedin-detailed', icon: '👔', label: 'LinkedIn Pro', section: 'channels' },
  { to: '/cold-call', icon: '📞', label: 'Cold Call', section: 'channels' },
  { to: '/cold-call-detailed', icon: '☎️', label: 'Call Center', section: 'channels' },
  { to: '/schedule', icon: '📅', label: 'Scheduler', section: 'automation' },
  { to: '/ai-responses', icon: '🤖', label: 'AI Response', section: 'automation' },
  { to: '/integrations', icon: '🔗', label: 'Integrations', section: 'automation' },
  { to: '/learning', icon: '🧠', label: 'Self-Learning', section: 'automation' },
  { to: '/dmca', icon: '⚖️', label: 'DMCA Tracker', section: 'automation' },
  { to: '/clients', icon: '👤', label: 'Clients', section: 'automation' },
  { to: '/team', icon: '🤖', label: 'Team', section: 'automation' },
  { to: '/revenue', icon: '💰', label: 'Revenue', section: 'automation' },
  { to: '/webhooks', icon: '🔌', label: 'Webhooks', section: 'automation' },
  { to: '/campaign-scheduler', icon: '⏰', label: 'Scheduler', section: 'automation' },
  { to: '/integrations-hub', icon: '🔗', label: 'Integrations Hub', section: 'automation' },
  { to: '/settings', icon: '⚙️', label: 'Settings', section: 'system' },
  { to: '/settings-detailed', icon: '🔧', label: 'System Settings', section: 'system' },
  { to: '/notifications', icon: '🔔', label: 'Notifications', section: 'system' },
  { to: '/audit-log', icon: '📋', label: 'Audit Log', section: 'system' },
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
