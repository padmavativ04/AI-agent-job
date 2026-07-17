import React from 'react';
import '../styles/Header.css';

function Header() {
  return (
    <header className="header">
      <div className="header-content">
        <div className="header-left">
          <h1 className="app-title">🤖 AI Job Agent</h1>
          <p className="app-tagline">Find and apply to jobs automatically</p>
        </div>
        <div className="header-right">
          <div className="status-badge">
            <span className="status-dot">●</span>
            Live & Ready
          </div>
        </div>
      </div>
    </header>
  );
}

export default Header;
