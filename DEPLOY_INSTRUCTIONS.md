# 🚀 Live Deployment Instructions

## Quick Links
- **GitHub Repo:** https://github.com/padmavativ04-create/AI-agent-job
- **Deploy Backend:** https://railway.app
- **Deploy Frontend:** https://vercel.com

---

## PART 1: Deploy Backend to Railway (5 min)

### Step 1: Sign Up at Railway
1. Go to https://railway.app
2. Click "Start Free"
3. Click "Continue with GitHub"
4. Authorize Railway to access your GitHub account
5. Click "Create New Project"

### Step 2: Connect Your Repository
1. Click "Deploy from GitHub repo"
2. Select your GitHub account
3. Search for "AI-agent-job"
4. Click to select it
5. Railway will auto-detect your Python app

### Step 3: Configure Build Settings
Railway should auto-detect:
```
Root Directory: /backend
```

If not, manually set:
1. Go to "Settings"
2. Set "Root Directory" to: `backend`

### Step 4: Set Environment Variables
1. Click "Variables" tab
2. Add these variables:
   ```
   FLASK_ENV=production
   PYTHON_VERSION=3.9
   ```
3. Click "Deploy"

### Step 5: Get Your Live URL
1. Wait for deployment (2-3 minutes)
2. Click "Deployments" 
3. Find the green checkmark deployment
4. Copy the URL (will be like: `https://your-app.railway.app`)
5. **Save this URL - you'll need it for frontend!**

### Step 6: Test Your Backend
Open in browser:
```
https://your-app.railway.app/
```

You should see:
```json
{
  "status": "online",
  "service": "AI Job Application Agent",
  ...
}
```

✅ **Backend is LIVE!**

---

## PART 2: Deploy Frontend to Vercel (5 min)

### Step 1: Create Frontend App (locally first)
```bash
cd "/Users/padmavativaidyanathan/Desktop/Claude code/AI-agent-job"
npx create-react-app frontend
cd frontend
npm install axios
```

### Step 2: Create React Component
Replace `src/App.js` with:

```jsx
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

  // UPDATE THIS with your Railway URL
  const BACKEND_URL = 'https://your-app.railway.app';

  const handleSearch = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.post(`${BACKEND_URL}/search`, preferences);
      setResults(response.data);
    } catch (err) {
      setError('Error searching jobs. Check your backend URL.');
      console.error(err);
    }
    setLoading(false);
  };

  return (
    <div className="App">
      <header className="header">
        <h1>🤖 AI Job Application Agent</h1>
        <p>Find and apply to jobs automatically</p>
      </header>

      <div className="container">
        <div className="form-section">
          <h2>Search Criteria</h2>
          
          <div className="form-group">
            <label>Job Titles (comma-separated)</label>
            <input
              type="text"
              value={preferences.titles.join(', ')}
              onChange={(e) => setPreferences({
                ...preferences,
                titles: e.target.value.split(',').map(t => t.trim())
              })}
              placeholder="Customer Success, Implementation Consultant"
            />
          </div>

          <div className="form-group">
            <label>Location</label>
            <input
              type="text"
              value={preferences.location}
              onChange={(e) => setPreferences({
                ...preferences,
                location: e.target.value
              })}
              placeholder="Canada"
            />
          </div>

          <div className="form-group">
            <label>Minimum Salary (CAD)</label>
            <input
              type="number"
              value={preferences.salary_min}
              onChange={(e) => setPreferences({
                ...preferences,
                salary_min: parseInt(e.target.value)
              })}
              placeholder="50000"
            />
          </div>

          <div className="form-group">
            <label>Your Goals</label>
            <textarea
              value={preferences.goals}
              onChange={(e) => setPreferences({
                ...preferences,
                goals: e.target.value
              })}
              placeholder="What do you want in a job?"
              rows="3"
            />
          </div>

          <button 
            onClick={handleSearch} 
            disabled={loading}
            className="search-btn"
          >
            {loading ? '🔍 Searching...' : '🚀 Search & Apply'}
          </button>
        </div>

        {error && (
          <div className="error">
            ❌ {error}
          </div>
        )}

        {results && (
          <div className="results-section">
            <h2>📊 Results</h2>
            
            <div className="stats">
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
              {results.jobs.map((job) => (
                <div key={job.id} className="job-card">
                  <div className="job-header">
                    <h4>{job.title}</h4>
                    <span className="match-score">{job.match_score}</span>
                  </div>
                  <p className="company">
                    {job.company} • {job.location}
                  </p>
                  <p className="salary">💰 ${job.salary.toLocaleString()} CAD</p>
                  <button className="apply-btn">Applied ✓</button>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      <footer>
        <p>Built with ❤️ using React + Python + AI</p>
      </footer>
    </div>
  );
}

export default App;
```

### Step 3: Add Styling
Replace `src/App.css` with:

```css
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
}

.App {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  background: rgba(0, 0, 0, 0.5);
  color: white;
  padding: 40px 20px;
  text-align: center;
}

.header h1 {
  font-size: 3em;
  margin-bottom: 10px;
}

.header p {
  font-size: 1.2em;
  opacity: 0.9;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
  flex: 1;
  width: 100%;
}

.form-section {
  background: white;
  border-radius: 10px;
  padding: 30px;
  margin-bottom: 30px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.form-section h2 {
  margin-bottom: 20px;
  color: #333;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #333;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 12px;
  border: 2px solid #e0e0e0;
  border-radius: 5px;
  font-size: 1em;
  font-family: inherit;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #667eea;
  background: #f8f9ff;
}

.search-btn {
  width: 100%;
  padding: 15px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 1.1em;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s;
}

.search-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
}

.search-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error {
  background: #fee;
  border: 2px solid #f88;
  color: #c00;
  padding: 15px;
  border-radius: 5px;
  margin-bottom: 20px;
}

.results-section {
  background: white;
  border-radius: 10px;
  padding: 30px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.results-section h2 {
  margin-bottom: 30px;
  color: #333;
}

.stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.stat-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 30px;
  border-radius: 10px;
  text-align: center;
}

.stat-card h3 {
  font-size: 2.5em;
  margin-bottom: 10px;
}

.stat-card p {
  font-size: 0.9em;
  opacity: 0.9;
}

.jobs-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.job-card {
  background: #f8f9ff;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  padding: 20px;
  transition: all 0.3s;
}

.job-card:hover {
  border-color: #667eea;
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.2);
}

.job-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  margin-bottom: 15px;
}

.job-card h4 {
  color: #333;
  font-size: 1.2em;
  flex: 1;
}

.match-score {
  background: #667eea;
  color: white;
  padding: 5px 15px;
  border-radius: 20px;
  font-size: 0.9em;
  font-weight: 600;
  white-space: nowrap;
  margin-left: 10px;
}

.company {
  color: #666;
  margin-bottom: 10px;
  font-size: 0.95em;
}

.salary {
  font-weight: 600;
  color: #667eea;
  margin-bottom: 15px;
}

.apply-btn {
  width: 100%;
  padding: 10px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: 600;
}

.apply-btn:hover {
  background: #764ba2;
}

footer {
  background: rgba(0, 0, 0, 0.8);
  color: white;
  text-align: center;
  padding: 20px;
  margin-top: 40px;
}

@media (max-width: 768px) {
  .header h1 {
    font-size: 2em;
  }

  .container {
    padding: 20px 15px;
  }

  .jobs-grid {
    grid-template-columns: 1fr;
  }
}
```

### Step 4: Deploy to Vercel
```bash
cd "/Users/padmavativaidyanathan/Desktop/Claude code/AI-agent-job/frontend"
npm install -g vercel
vercel
```

Follow prompts:
- Confirm project name
- Select "Create React App"
- Accept defaults
- Deploy to production: YES

### Step 5: Update Backend URL in Frontend
1. After Vercel deployment completes, you'll get your frontend URL
2. Go back to your Railway backend
3. Copy the Railway URL
4. In Vercel dashboard, go to "Settings" → "Environment Variables"
5. No wait - update it in your code instead:

```bash
# In frontend/src/App.js, line 15:
const BACKEND_URL = 'https://your-railway-app.railway.app';

# Then redeploy:
cd frontend
vercel --prod
```

---

## PART 3: Test Your Live Application

### Test 1: Frontend is Live
Open your Vercel URL in browser:
```
https://your-frontend.vercel.app
```

### Test 2: Search for Jobs
1. Enter job titles: "Customer Success, Implementation Consultant"
2. Location: "Canada"
3. Salary: "50000"
4. Click "Search & Apply"
5. Should see results!

### Test 3: Backend API
```bash
curl https://your-backend.railway.app/stats
```

---

## Deployment Summary

✅ **Backend:** Live on Railway  
✅ **Frontend:** Live on Vercel  
✅ **Database:** Optional (Phase 4)  
✅ **Custom Domain:** Optional (add your domain)

---

## Troubleshooting

### Issue: "Cannot find module 'complete_agent'"
**Fix:** Make sure all Python files are in `/backend`

### Issue: "CORS error" on frontend
**Fix:** Backend URL should have no trailing slash:
```
✅ https://your-app.railway.app
❌ https://your-app.railway.app/
```

### Issue: Frontend not updating
**Fix:** Redeploy to Vercel:
```bash
cd frontend
vercel --prod --force
```

---

## What's Deployed

- ✅ AI Job Application Agent
- ✅ Multi-agent architecture
- ✅ Semantic job matching
- ✅ REST API
- ✅ React frontend
- ✅ Automatic job search & apply

## Next Features to Add

1. **Database** - Store applications
2. **Authentication** - User accounts
3. **Dashboard** - Track all applications
4. **Real APIs** - Connect LinkedIn, Indeed
5. **Webhooks** - Notifications when jobs respond
6. **Mobile App** - React Native version

---

**Your AI Job Agent is LIVE! 🚀**

