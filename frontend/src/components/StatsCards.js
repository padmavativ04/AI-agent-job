import React from 'react';
import '../styles/StatsCards.css';

function StatsCards({ stats }) {
  const cards = [
    { icon: '🔍', label: 'Jobs Found', value: stats.total_jobs },
    { icon: '📝', label: 'Applications', value: stats.total_applications },
    { icon: '📧', label: 'Follow-ups', value: stats.total_emails },
  ];

  return (
    <div className="stats-grid">
      {cards.map((card, idx) => (
        <div key={idx} className="stat-card">
          <div className="stat-icon">{card.icon}</div>
          <div className="stat-content">
            <h3 className="stat-value">{card.value}</h3>
            <p className="stat-label">{card.label}</p>
          </div>
        </div>
      ))}
    </div>
  );
}

export default StatsCards;
