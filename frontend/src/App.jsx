import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import LaunchTask from './pages/LaunchTask';
import LeadDatabase from './pages/LeadDatabase';
import EmailAccounts from './pages/EmailAccounts';
import Analytics from './pages/Analytics';
import TaskManager from './pages/TaskManager';
import HotLeads from './pages/HotLeads';
import Settings from './pages/Settings';
import CeoDashboard from './pages/CeoDashboard';
import Sidebar from './components/Sidebar';

export default function App() {
  return (
    <BrowserRouter>
      <div className="flex min-h-screen bg-dark-900">
        <Sidebar />
        <main className="flex-1 p-6 ml-64">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/launch-task" element={<LaunchTask />} />
            <Route path="/leads" element={<LeadDatabase />} />
            <Route path="/email-accounts" element={<EmailAccounts />} />
            <Route path="/analytics" element={<Analytics />} />
            <Route path="/tasks" element={<TaskManager />} />
            <Route path="/hot-leads" element={<HotLeads />} />
            <Route path="/settings" element={<Settings />} />
            <Route path="/ceo" element={<CeoDashboard />} />
            <Route path="*" element={<Navigate to="/" />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}
