import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Header from './src/components/Header';
import Footer from './src/Footer';
import Dashboard from './src/pages/Dashboard';
import LaunchTask from './src/pages/LaunchTask';
import LeadDatabase from './src/pages/LeadDatabase';
import EmailAccounts from './src/pages/EmailAccounts';
import Analytics from './src/pages/Analytics';
import TaskManager from './src/pages/TaskManager';
import HotLeads from './src/pages/HotLeads';
import Settings from './src/pages/Settings';
import './src/App.css';

function App() {
  return (
    <BrowserRouter>
      <div className="App">
        <Header />
        <main>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/launch" element={<LaunchTask />} />
            <Route path="/leads" element={<LeadDatabase />} />
            <Route path="/accounts" element={<EmailAccounts />} />
            <Route path="/analytics" element={<Analytics />} />
            <Route path="/tasks" element={<TaskManager />} />
            <Route path="/hot-leads" element={<HotLeads />} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </BrowserRouter>
  );
}

export default App;
