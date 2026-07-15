# Deployment Guide - AI Job Application Agent

## 🚀 Quick Start (5 minutes)

### Prerequisites
- GitHub account (you have this ✓)
- Railway account (free at railway.app)
- Node.js (for frontend)

---

## Part 1: Backend Deployment (Railway)

### Step 1: Create Railway Account
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub (click "Deploy with GitHub")
3. Authorize Railway to access your GitHub

### Step 2: Deploy Backend
1. In Railway dashboard, click "New Project"
2. Select "Deploy from GitHub"
3. Choose your repo: `AI-agent-job`
4. Select the `backend/` directory
5. Railway will detect `requirements.txt` automatically

### Step 3: Configure Environment
1. Go to "Variables" tab
2. Add:
   ```
   FLASK_ENV=production
   PORT=5000
   ```

### Step 4: Get Your Backend URL
After deployment:
- Your API will be at: `https://your-app.railway.app`
- Test it: `https://your-app.railway.app/`

---

## Part 2: API Endpoints

Once deployed, you can call your agent from anywhere:

### 1. Health Check
```bash
curl https://your-app.railway.app/
```

### 2. Search for Jobs
```bash
curl -X POST https://your-app.railway.app/search \
  -H "Content-Type: application/json" \
  -d '{
    "titles": ["Customer Success", "Implementation Consultant"],
    "location": "Canada",
    "salary_min": 50000,
    "goals": "Help customers and solve problems"
  }'
```

### 3. Get Statistics
```bash
curl https://your-app.railway.app/stats
```

### 4. Get Applications
```bash
curl https://your-app.railway.app/applications
```

---

## Part 3: Frontend Deployment (Vercel)

### Step 1: Create Frontend Boilerplate
```bash
cd /Users/padmavativaidyanathan/Desktop/Claude\ code/AI-agent-job
npx create-react-app frontend
cd frontend
```

### Step 2: Create Frontend Component
Create `src/App.js`:
```jsx
import React, { useState } from 'react';
import './App.css';

function App() {
  const [preferences, setPreferences] = useState({
    titles: ['Customer Success'],
    location: 'Canada',
    salary_min: 50000,
    goals: 'Help customers'
  });
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    setLoading(true);
    try {
      const response = await fetch('https://your-app.railway.app/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(preferences)
      });
      const data = await response.json();
      setResults(data);
    } catch (error) {
      console.error('Error:', error);
    }
    setLoading(false);
  };

  return (
    <div className="App">
      <h1>🤖 AI Job Application Agent</h1>
      
      <div className="form">
        <input
          type="text"
          placeholder="Job titles (comma separated)"
          onChange={(e) => setPreferences({
            ...preferences,
            titles: e.target.value.split(',').map(t => t.trim())
          })}
        />
        
        <input
          type="number"
          placeholder="Minimum salary (CAD)"
          onChange={(e) => setPreferences({
            ...preferences,
            salary_min: parseInt(e.target.value)
          })}
        />
        
        <button onClick={handleSearch} disabled={loading}>
          {loading ? 'Searching...' : 'Search Jobs'}
        </button>
      </div>

      {results && (
        <div className="results">
          <h2>Results</h2>
          <p>Jobs Found: {results.total_jobs}</p>
          <p>Applications Made: {results.total_applications}</p>
          
          <h3>Top Opportunities</h3>
          {results.jobs.map((job) => (
            <div key={job.id} className="job-card">
              <h4>{job.title}</h4>
              <p>{job.company} • {job.location}</p>
              <p>💰 ${job.salary} CAD</p>
              <p>Match: {job.match_score}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;
```

### Step 3: Deploy to Vercel
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel
```

Follow the prompts:
- Project name: `ai-job-agent-frontend`
- Framework: `Create React App`
- Deploy to production: `yes`

---

## Part 4: Git Workflow

### Stage 1: Commit Changes
```bash
cd /Users/padmavativaidyanathan/Desktop/Claude\ code/AI-agent-job
git add .
git commit -m "Add Flask backend and deployment configs

- Add app.py with Flask API endpoints
- Add flask-cors and gunicorn to requirements
- Add deployment guide
- Ready for production deployment"
```

### Stage 2: Push to GitHub
```bash
git push -u origin main
```

### Stage 3: Verify on GitHub
1. Go to https://github.com/padmavativ04-create/AI-agent-job
2. Confirm all files are there
3. You should see:
   - `backend/app.py`
   - `backend/requirements.txt`
   - `backend/complete_agent.py`
   - `DEPLOYMENT.md`

---

## Testing Your Deployed Agent

### Test 1: Health Check
```bash
curl https://your-app.railway.app/
# Expected: {"status": "online", ...}
```

### Test 2: Search for Jobs
```bash
curl -X POST https://your-app.railway.app/search \
  -H "Content-Type: application/json" \
  -d '{
    "titles": ["Customer Success", "Tech Support"],
    "location": "Canada",
    "salary_min": 50000,
    "goals": "Help customers"
  }'
```

### Test 3: Get Statistics
```bash
curl https://your-app.railway.app/stats
```

---

## Environment Variables

Create `.env` in backend/:
```
FLASK_ENV=production
PORT=5000
```

---

## Troubleshooting

### Issue: "Module not found"
**Solution:** Make sure `complete_agent.py` is in the same directory as `app.py`

### Issue: "CORS error"
**Solution:** Make sure `flask-cors` is installed and imported in `app.py`

### Issue: "Port already in use"
**Solution:** Kill the process: `lsof -i :5000` then `kill -9 <PID>`

---

## Next Steps

✅ Backend deployed on Railway
✅ Frontend deployed on Vercel
✅ API accessible worldwide

### What's Next?
1. **Add Database** - Store applications in PostgreSQL
2. **Add Authentication** - User accounts and login
3. **Add Dashboard** - Track all applications
4. **Add Real APIs** - Connect LinkedIn, Indeed, Glassdoor
5. **Add Voice** - Speak to your agent

---

## Support

- Railway Docs: https://docs.railway.app
- Vercel Docs: https://vercel.com/docs
- Flask Docs: https://flask.palletsprojects.com

---

**Your agent is live! 🚀**
