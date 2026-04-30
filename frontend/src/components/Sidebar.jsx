import React, { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import {
  LayoutDashboard, Play, Users, Mail, BarChart3,
  ListTodo, Flame, Settings, Shield,
} from 'lucide-react'

const navItems = [
  { path: '/', icon: LayoutDashboard, label: 'Dashboard' },
  { path: '/launch-task', icon: Play, label: 'Launch Task' },
  { path: '/leads', icon: Users, label: 'Lead Database' },
  { path: '/email-accounts', icon: Mail, label: 'Email Accounts' },
  { path: '/analytics', icon: BarChart3, label: 'Analytics' },
  { path: '/tasks', icon: ListTodo, label: 'Task Manager' },
  { path: '/hot-leads', icon: Flame, label: 'Hot Leads', highlight: true },
  { path: '/settings', icon: Settings, label: 'Settings' },
  { path: '/ceo', icon: Shield, label: 'CEO Dashboard', highlight: true },
]

const departments = [
  { name: 'CEO', status: 'online' },
  { name: 'Scraping', status: 'online' },
  { name: 'Validation', status: 'online' },
  { name: 'Marketing', status: 'online' },
  { name: 'Email Sending', status: 'online' },
  { name: 'Tracking', status: 'online' },
  { name: 'Sales', status: 'online' },
  { name: 'JARVIS', status: 'online' },
  { name: 'Memory', status: 'online' },
]

export default function Sidebar() {
  const location = useLocation()

  return (
    <aside className="fixed left-0 top-0 h-screen w-64 bg-dark-800 border-r border-dark-600 flex flex-col">
      <div className="p-6 border-b border-dark-600">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-accent-purple to-accent-cyan flex items-center justify-center">
            <Shield className="w-5 h-5 text-white" />
          </div>
          <div>
            <h1 className="font-bold text-lg">DMCAShield</h1>
            <p className="text-xs text-gray-500">Control Tower</p>
          </div>
        </div>
      </div>

      <nav className="flex-1 p-4 space-y-1 overflow-y-auto">
        {navItems.map(({ path, icon: Icon, label, highlight }) => (
          <Link
            key={path}
            to={path}
            className={`flex items-center gap-3 px-4 py-3 rounded-xl transition-all ${
              location.pathname === path
                ? 'bg-accent-purple/20 text-accent-purple border border-accent-purple/30'
                : highlight
                ? 'bg-accent-red/10 text-accent-red border border-accent-red/30 hover:bg-accent-red/20'
                : 'text-gray-400 hover:bg-dark-700 hover:text-white'
            }`}
          >
            <Icon className="w-5 h-5" />
            <span className="font-medium">{label}</span>
          </Link>
        ))}
      </nav>

      <div className="p-4 border-t border-dark-600">
        <div className="text-xs text-gray-500 mb-3 uppercase tracking-wider font-semibold">
          Departments
        </div>
        <div className="grid grid-cols-2 gap-2">
          {departments.map((dept) => (
            <div key={dept.name} className="flex items-center gap-2 text-xs text-gray-400">
              <span className={`department-dot ${dept.status}`}></span>
              <span className="truncate">{dept.name}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="p-4 border-t border-dark-600">
        <div className="glass-card p-4">
          <div className="flex items-center gap-2 text-xs text-accent-green mb-2">
            <Shield className="w-4 h-4" />
            <span className="font-semibold">System Status</span>
          </div>
          <div className="text-2xl font-bold">Operational</div>
          <div className="text-xs text-gray-500">12 departments online</div>
        </div>
      </div>
    </aside>
  )
}