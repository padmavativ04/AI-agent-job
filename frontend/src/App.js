import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import Header from './components/Header';
import SearchForm from './components/SearchForm';
import StatsCards from './components/StatsCards';
import JobCard from './components/JobCard';

function App() {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [backendConnected, setBackendConnected] = useState(false);

  const BACKEND_URL = 'http://localhost:5000';

  // Check backend connection on component mount
  useEffect(() => {
    checkBackendConnection();
  }, []);

  const checkBackendConnection = async () => {
    try {
      const response = await axios.get(`${BACKEND_URL}/`, {
        timeout: 3000,
      });
      if (response.status === 200) {
        setBackendConnected(true);
        setError(null);
        console.log('✅ Backend connected:', response.data);
      }
    } catch (err) {
      console.error('Backend connection failed:', err.message);
      setBackendConnected(false);
      setError(
        `⚠️ Cannot connect to backend at ${BACKEND_URL}\n\nMake sure:\n1. Terminal 1 is running: python3 app.py\n2. Backend shows "Running on http://127.0.0.1:5000"`
      );
    }
  };

  const handleSearch = async (preferences) => {
    setLoading(true);
    setError(null);
    setResults(null);

    try {
      console.log('Searching with preferences:', preferences);

      const response = await axios.post(`${BACKEND_URL}/search`, preferences, {
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
        },
        timeout: 10000,
      });

      console.log('Results received:', response.data);
      setResults(response.data);
      setBackendConnected(true);
    } catch (err) {
      console.error('Error:', err);
      console.error('Error details:', {
        message: err.message,
        response: err.response?.status,
        code: err.code,
      });
      setBackendConnected(false);
      setError(
        `⚠️ Connection Error: Cannot reach backend at ${BACKEND_URL}\n\nError: ${err.message}\n\nFix:\n1. Check Terminal 1 shows "Running on http://127.0.0.1:5000"\n2. Make sure python3 app.py is running\n3. If port 5000 is in use, run: lsof -i :5000 | grep LISTEN | awk '{print $2}' | xargs kill -9`
      );
    }

    setLoading(false);
  };

  return (
    <div className="App">
      <Header />

      <main className="main-content">
        <SearchForm onSearch={handleSearch} loading={loading} />

        {error && (
          <div className="error-banner">
            <h3>⚠️ Backend Connection Error</h3>
            <p style={{ whiteSpace: 'pre-wrap', textAlign: 'left' }}>
              {error}
            </p>
            <div style={{ marginTop: '20px', padding: '15px', backgroundColor: 'rgba(0,0,0,0.1)', borderRadius: '5px' }}>
              <strong>Quick Fix:</strong>
              <p>Terminal 1 (if not already running):</p>
              <code style={{ display: 'block', backgroundColor: 'rgba(0,0,0,0.2)', padding: '10px', borderRadius: '3px', marginTop: '5px' }}>
                cd "/Users/padmavativaidyanathan/Desktop/Claude code/AI-agent-job/backend" && python3 app.py
              </code>
              <p style={{ marginTop: '10px' }}>Then refresh this page (F5)</p>
            </div>
          </div>
        )}

        {backendConnected && !error && results === null && (
          <div style={{ textAlign: 'center', padding: '20px', color: '#4caf50' }}>
            ✅ Backend Connected
          </div>
        )}

        {results && (
          <div className="results-container">
            <StatsCards stats={results} />

            <div className="results-section">
              <h2>🏆 Top Opportunities</h2>

              {results.jobs && results.jobs.length > 0 ? (
                <div className="jobs-grid">
                  {results.jobs.map((job) => (
                    <JobCard key={job.id} job={job} />
                  ))}
                </div>
              ) : (
                <div className="no-results">
                  <p>No jobs found matching your criteria</p>
                </div>
              )}
            </div>

            {results.applications && results.applications.length > 0 && (
              <div className="applications-section">
                <h2>📧 Applications Sent</h2>
                <div className="applications-list">
                  {results.applications.slice(0, 10).map((app, idx) => (
                    <div key={idx} className="application-item">
                      <div className="app-info">
                        <span className="app-company">{app.company}</span>
                        <span className="app-role">{app.job_title}</span>
                      </div>
                      <div className="app-meta">
                        <span className="app-salary">
                          ${app.salary.toLocaleString()}
                        </span>
                        <span className="app-status">✓ {app.status}</span>
                      </div>
                    </div>
                  ))}
                  {results.applications.length > 10 && (
                    <p className="more-text">
                      +{results.applications.length - 10} more applications
                    </p>
                  )}
                </div>
              </div>
            )}
          </div>
        )}

        {!results && !error && (
          <div className="welcome-section">
            <div className="welcome-content">
              <h2>Welcome to Your AI Job Agent 🤖</h2>
              <p className="welcome-intro">
                Powered by AI to find and apply to jobs automatically
              </p>

              <div className="features-grid">
                <div className="feature-card">
                  <span className="feature-icon">🔍</span>
                  <h3>Smart Search</h3>
                  <p>Find jobs matching your criteria instantly</p>
                </div>

                <div className="feature-card">
                  <span className="feature-icon">🤖</span>
                  <h3>AI Matching</h3>
                  <p>Semantic matching with machine learning</p>
                </div>

                <div className="feature-card">
                  <span className="feature-icon">📝</span>
                  <h3>Auto Apply</h3>
                  <p>Apply to multiple jobs in seconds</p>
                </div>

                <div className="feature-card">
                  <span className="feature-icon">📧</span>
                  <h3>Follow-ups</h3>
                  <p>Send professional follow-up emails</p>
                </div>

                <div className="feature-card">
                  <span className="feature-icon">📊</span>
                  <h3>Reports</h3>
                  <p>Get comprehensive results summary</p>
                </div>

                <div className="feature-card">
                  <span className="feature-icon">⚡</span>
                  <h3>Fast & Easy</h3>
                  <p>Automation that saves you hours</p>
                </div>
              </div>

              <div className="tech-stack">
                <h3>Built With</h3>
                <div className="tech-badges">
                  <span className="tech-badge">React</span>
                  <span className="tech-badge">Python</span>
                  <span className="tech-badge">Flask</span>
                  <span className="tech-badge">AI/ML</span>
                </div>
              </div>

              <p className="welcome-cta">
                Enter your preferences above and let the AI find your perfect job!
              </p>
            </div>
          </div>
        )}
      </main>

      <footer className="app-footer">
        <p>🚀 AI Job Application Agent v1.0</p>
        <p>Built with ❤️ using Python, React, and Machine Learning</p>
        <p style={{ marginTop: '10px', fontSize: '0.9em', opacity: 0.8 }}>
          Backend: <code>{BACKEND_URL}</code>
        </p>
      </footer>
    </div>
  );
}

export default App;
