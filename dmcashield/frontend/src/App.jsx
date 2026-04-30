import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import JARVIS from './components/JARVIS';
import Dashboard from './pages/Dashboard';
import LaunchTask from './pages/LaunchTask';
import LeadDatabase from './pages/LeadDatabase';
import EmailAccounts from './pages/EmailAccounts';
import Analytics from './pages/Analytics';
import TaskManager from './pages/TaskManager';
import HotLeads from './pages/HotLeads';
import Settings from './pages/Settings';
import CampaignManager from './pages/CampaignManager';
import EmailWarmup from './pages/EmailWarmup';
import AIResponseHandler from './pages/AIResponseHandler';
import CampaignScheduler from './pages/CampaignScheduler';
import Integrations from './pages/Integrations';
import SelfLearning from './pages/SelfLearning';
import SMSCampaign from './pages/SMSCampaign';
import WhatsAppCampaign from './pages/WhatsAppCampaign';
import LinkedInOutreach from './pages/LinkedInOutreach';
import ColdCalling from './pages/ColdCalling';
import './styles/design-system.css';

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function App() {
  const [systemStatus, setSystemStatus] = useState('connecting');
  const [hotLeadCount, setHotLeadCount] = useState(0);

  useEffect(() => {
    // Initial health check
    fetch(`${API}/health`)
      .then(r => r.json())
      .then(d => setSystemStatus(d.status || 'operational'))
      .catch(() => setSystemStatus('offline'));

    // WebSocket for real-time updates
    let ws;
    const connectWS = () => {
      ws = new WebSocket('ws://localhost:8000/ws');
      ws.onopen = () => setSystemStatus('operational');
      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          if (data.type === 'system_status') {
            setSystemStatus(data.data?.status || 'operational');
          }
        } catch (e) {}
      };
      ws.onclose = () => {
        setSystemStatus('reconnecting');
        setTimeout(connectWS, 5000);
      };
      ws.onerror = () => ws.close();
    };
    connectWS();

    // Poll hot lead count
    const pollHot = setInterval(() => {
      fetch(`${API}/api/hot-leads`).then(r => r.json()).then(d => setHotLeadCount(d.length)).catch(() => {});
    }, 30000);

    return () => {
      if (ws) ws.close();
      clearInterval(pollHot);
    };
  }, []);

  return (
    <BrowserRouter>
      <div className="app-layout">
        <Sidebar systemStatus={systemStatus} hotLeadCount={hotLeadCount} />
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/launch" element={<LaunchTask />} />
          <Route path="/leads" element={<LeadDatabase />} />
          <Route path="/accounts" element={<EmailAccounts />} />
          <Route path="/analytics" element={<Analytics />} />
          <Route path="/tasks" element={<TaskManager />} />
          <Route path="/campaigns" element={<CampaignManager />} />
          <Route path="/warmup" element={<EmailWarmup />} />
          <Route path="/ai-responses" element={<AIResponseHandler />} />
          <Route path="/schedule" element={<CampaignScheduler />} />
          <Route path="/integrations" element={<Integrations />} />
          <Route path="/learning" element={<SelfLearning />} />
          <Route path="/sms" element={<SMSCampaign />} />
          <Route path="/whatsapp" element={<WhatsAppCampaign />} />
          <Route path="/linkedin" element={<LinkedInOutreach />} />
          <Route path="/cold-call" element={<ColdCalling />} />
          <Route path="/hot-leads" element={<HotLeads />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
        <JARVIS />
      </div>
    </BrowserRouter>
  );
}
