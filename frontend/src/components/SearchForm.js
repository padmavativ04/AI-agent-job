import React, { useState } from 'react';
import '../styles/SearchForm.css';

function SearchForm({ onSearch, loading }) {
  const [preferences, setPreferences] = useState({
    titles: ['Customer Success'],
    location: 'Canada',
    salary_min: 50000,
    goals: 'Help customers succeed',
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch(preferences);
  };

  const handleTitleChange = (e) => {
    const titles = e.target.value
      .split(',')
      .map((t) => t.trim())
      .filter((t) => t);
    setPreferences({ ...preferences, titles });
  };

  return (
    <div className="search-form-container">
      <form onSubmit={handleSubmit} className="search-form">
        <h2>🔍 Find Your Perfect Job</h2>

        <div className="form-group">
          <label htmlFor="titles">Job Titles (comma-separated)</label>
          <input
            id="titles"
            type="text"
            value={preferences.titles.join(', ')}
            onChange={handleTitleChange}
            placeholder="Customer Success, Implementation Consultant, Project Manager"
            className="form-input"
          />
          <small>Examples: Customer Success, Tech Support, Solutions Consultant</small>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="location">Location</label>
            <input
              id="location"
              type="text"
              value={preferences.location}
              onChange={(e) =>
                setPreferences({ ...preferences, location: e.target.value })
              }
              placeholder="Canada"
              className="form-input"
            />
          </div>

          <div className="form-group">
            <label htmlFor="salary">Min Salary (CAD)</label>
            <input
              id="salary"
              type="number"
              value={preferences.salary_min}
              onChange={(e) =>
                setPreferences({
                  ...preferences,
                  salary_min: parseInt(e.target.value),
                })
              }
              placeholder="50000"
              className="form-input"
            />
          </div>
        </div>

        <div className="form-group">
          <label htmlFor="goals">Your Career Goals</label>
          <textarea
            id="goals"
            value={preferences.goals}
            onChange={(e) =>
              setPreferences({ ...preferences, goals: e.target.value })
            }
            placeholder="What do you want in a job? Help customers? Solve technical problems? Learn new technologies?"
            rows="3"
            className="form-input"
          />
          <small>This helps AI match you to better opportunities</small>
        </div>

        <button type="submit" disabled={loading} className="btn-primary">
          {loading ? '🔍 Searching...' : '🚀 Search & Apply'}
        </button>
      </form>
    </div>
  );
}

export default SearchForm;
