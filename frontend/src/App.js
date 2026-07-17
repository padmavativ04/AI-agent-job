import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [preferences, setPreferences] = useState({
    titles: ['Customer Success'],
    location: 'Canada',
    salary_min: 50000,
    goals: 'Help customers succeed'
  });

  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Backend URL - change this if running on different port
  const BACKEND_URL = 'http://localhost:5000';

  const handleSearch = async () => {
    setLoading(true);
    setError(null);

    try {
      console.log('Searching with preferences:', preferences);

      const response = await axios.post(`${BACKEND_URL}/search`, preferences, {
        headers: {
          'Content-Type': 'application/json',
        },
      });

      console.log('Results received:', response.data);
      setResults(response.data);
    } catch (err) {
      console.error('Error:', err);
      setError(`Error: ${err.message}. Make sure backend is running at ${BACKEND_URL}`);
    }

    setLoading(false);
  };

  const handleTitleChange = (e) => {
    const titles = e.target.value.split(',').map((t) => t.trim()).filter((t) => t);
    setPreferences({ ...preferences, titles });
  };

  return (
    <div className="App">
      <header className="header">
        <h1>🤖 AI Job Application Agent</h1>
        <p>Find and apply to jobs automatically using AI</p>
      </header>

      <div className="container">
        <div className="form-section">
          <h2>🔍 Search Criteria</h2>

          <div className="form-group">
            <label>Job Titles (comma-separated)</label>
            <input
              type="text"
              value={preferences.titles.join(', ')}
              onChange={handleTitleChange}
              placeholder="Customer Success, Implementation Consultant, Project Manager"
              className="input"
            />
            <small>Examples: Customer Success, Implementation Consultant, Tech Support</small>
          </div>

          <div className="form-group">
            <label>Location</label>
            <input
              type="text"
              value={preferences.location}
              onChange={(e) =>
                setPreferences({ ...preferences, location: e.target.value })
              }
              placeholder="Canada"
              className="input"
            />
            <small>Examples: Canada, Remote, Toronto</small>
          </div>

          <div className="form-group">
            <label>Minimum Salary (CAD)</label>
            <input
              type="number"
              value={preferences.salary_min}
              onChange={(e) =>
                setPreferences({ ...preferences, salary_min: parseInt(e.target.value) })
              }
              placeholder="50000"
              className="input"
            />
            <small>Your minimum acceptable salary</small>
          </div>

          <div className="form-group">
            <label>Your Career Goals</label>
            <textarea
              value={preferences.goals}
              onChange={(e) => setPreferences({ ...preferences, goals: e.target.value })}
              placeholder="What do you want in a job? Help customers? Solve technical problems? Learn new tech?"
              rows="3"
              className="textarea"
            />
            <small>This helps the AI match you to better opportunities</small>
          </div>

          <button
            onClick={handleSearch}
            disabled={loading}
            className="search-btn"
          >
            {loading ? '🔍 Searching...' : '🚀 Search & Apply'}
          </button>

          <div className="backend-status">
            Backend: <span className="status-online">● Online</span>
            {BACKEND_URL}
          </div>
        </div>

        {error && (
          <div className="error-section">
            <h3>❌ Error</h3>
            <p>{error}</p>
            <p>Make sure backend is running:</p>
            <code>python3 app.py</code>
          </div>
        )}

        {results && (
          <div className="results-section">
            <h2>📊 Results</h2>

            <div className="stats-grid">
              <div className="stat-card">
                <h3>{results.total_jobs}</h3>
                <p>Jobs Found</p>
              </div>
              <div className="stat-card">
                <h3>{results.total_applications}</h3>
                <p>Applications Made</p>
              </div>
              <div className="stat-card">
                <h3>{results.total_emails}</h3>
                <p>Follow-ups Sent</p>
              </div>
            </div>

            <h3>🏆 Top Opportunities</h3>
            <div className="jobs-grid">
              {results.jobs && results.jobs.length > 0 ? (
                results.jobs.map((job) => (
                  <div key={job.id} className="job-card">
                    <div className="job-header">
                      <h4>{job.title}</h4>
                      <span className="match-badge">{job.match_score}</span>
                    </div>
                    <p className="company">
                      {job.company} • {job.location}
                    </p>
                    <p className="salary">💰 ${job.salary.toLocaleString()} CAD</p>
                    <div className="job-footer">
                      <button className="apply-btn">✓ Applied</button>
                    </div>
                  </div>
                ))
              ) : (
                <p>No jobs found</p>
              )}
            </div>

            <h3>📧 Applications Summary</h3>
            <div className="applications-list">
              {results.applications && results.applications.length > 0 ? (
                results.applications.slice(0, 5).map((app, idx) => (
                  <div key={idx} className="application-item">
                    <span className="app-company">{app.company}</span>
                    <span className="app-role">{app.job_title}</span>
                    <span className="app-status">✓ {app.status}</span>
                  </div>
                ))
              ) : (
                <p>No applications yet</p>
              )}
              {results.applications && results.applications.length > 5 && (
                <p className="more-text">
                  +{results.applications.length - 5} more applications
                </p>
              )}
            </div>
          </div>
        )}

        {!results && !error && !loading && (
          <div className="welcome-section">
            <h2>👋 Welcome to Your AI Job Agent</h2>
            <p>
              This agent will:
            </p>
            <ul>
              <li>🔍 Search for jobs matching your criteria</li>
              <li>🤖 Use AI to find the best semantic matches</li>
              <li>📝 Apply to all matching jobs automatically</li>
              <li>📧 Send follow-up emails to companies</li>
              <li>📊 Generate a summary report</li>
            </ul>
            <p>
              <strong>Built with:</strong> Python • Flask • React • AI/ML
            </p>
          </div>
        )}
      </div>

      <footer>
        <p>
          🚀 AI Job Application Agent v1.0 • Built with ❤️ using Python, React, and AI
        </p>
        <p style={{ fontSize: '0.9em', marginTop: '10px' }}>
          Backend: <code>{BACKEND_URL}</code>
        </p>
      </footer>
    </div>
  );
}

export default App;
