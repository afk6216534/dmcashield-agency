import React from 'react';
import { Link } from 'react-router-dom';

function Header() {
  return (
    <header className="header">
      <h1 className="logo">DMCAShield</h1>
      <nav className="nav-bar">
        <Link to="/">Dashboard</Link>
        <Link to="/launch">Launch Task</Link>
        <Link to="/leads">Leads</Link>
        <Link to="/accounts">Accounts</Link>
        <Link to="/analytics">Analytics</Link>
        <Link to="/tasks">Tasks</Link>
        <Link to="/hot-leads">Hot Leads</Link>
        <Link to="/settings">Settings</Link>
      </nav>
    </header>
  );
}

export default Header;