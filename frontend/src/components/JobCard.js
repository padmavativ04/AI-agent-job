import React from 'react';
import '../styles/JobCard.css';

function JobCard({ job }) {
  return (
    <div className="job-card">
      <div className="job-card-header">
        <div className="job-info">
          <h4 className="job-title">{job.title}</h4>
          <p className="job-company">{job.company}</p>
        </div>
        <span className="match-badge">{job.match_score}</span>
      </div>

      <div className="job-details">
        <p className="location">📍 {job.location}</p>
        <p className="salary">💰 ${job.salary.toLocaleString()} CAD/year</p>
      </div>

      <div className="job-description">
        <p>{job.description || 'Exciting opportunity'}</p>
      </div>

      <div className="job-actions">
        <button className="btn-apply">✓ Applied</button>
        <button className="btn-details">Learn More</button>
      </div>
    </div>
  );
}

export default JobCard;
