# 🏠 Local Development Setup (Localhost)

Run your AI Job Agent on **http://localhost:5000** (backend) and **http://localhost:3000** (frontend)

---

## Quick Start (5 minutes)

### Terminal 1: Start Backend Server

```bash
cd "/Users/padmavativaidyanathan/Desktop/Claude code/AI-agent-job/backend"
pip install -r requirements.txt
python3 app.py
```

You'll see:
```
🚀 Starting Flask server...
📍 Backend running at: http://127.0.0.1:5000
Press CTRL+C to stop
```

✅ **Backend is ready at http://localhost:5000**

---

### Terminal 2: Start Frontend Server

```bash
cd "/Users/padmavativaidyanathan/Desktop/Claude code/AI-agent-job/frontend"
npm install
npm start
```

You'll see:
```
Compiled successfully!
You can now view the app in the browser.
  Local: http://localhost:3000
```

✅ **Frontend automatically opens at http://localhost:3000**

---

## 🎯 Test Your App

### Test 1: Backend Health Check
Open in browser or terminal:
```bash
curl http://localhost:5000/
```

Expected response:
```json
{
  "status": "online",
  "service": "AI Job Application Agent",
  "version": "1.0.0"
}
```

### Test 2: Search for Jobs (API)
```bash
curl -X POST http://localhost:5000/search \
  -H "Content-Type: application/json" \
  -d '{
    "titles": ["Customer Success", "Implementation Consultant"],
    "location": "Canada",
    "salary_min": 50000,
    "goals": "Help customers and solve problems"
  }'
```

Expected response:
```json
{
  "status": "success",
  "total_jobs": 13,
  "total_applications": 13,
  "jobs": [
    {
      "id": 1,
      "title": "Customer Success Manager",
      "company": "Shopify",
      "salary": 65000,
      "match_score": "98%"
    }
  ]
}
```

### Test 3: Get Statistics
```bash
curl http://localhost:5000/stats
```

Expected response:
```json
{
  "status": "success",
  "stats": {
    "searches_performed": 1,
    "applications_made": 13,
    "emails_sent": 13
  }
}
```

### Test 4: Frontend in Browser
1. Go to http://localhost:3000
2. Enter your preferences:
   - Job Titles: "Customer Success, Implementation Consultant"
   - Location: "Canada"
   - Salary: "50000"
   - Goals: "Help customers"
3. Click "Search & Apply"
4. See results instantly!

---

## 🛠️ Common Commands

### Stop Backend Server
Press `CTRL+C` in Terminal 1

### Stop Frontend Server
Press `CTRL+C` in Terminal 2

### Restart Everything
```bash
# Kill any running processes
pkill -f "python3 app.py"
pkill -f "npm start"

# Then restart both terminals
```

### View Backend Logs
Terminal 1 shows all requests:
```
127.0.0.1 - - [17/Jul/2026 12:25:07] "POST /search HTTP/1.1" 200
```

### View Frontend Errors
Terminal 2 shows compilation errors:
```
[31m✖ ESLint error[0m
```

---

## 📊 Folder Structure

```
AI-agent-job/
├── backend/               ← Python Flask server (port 5000)
│   ├── app.py            (main API)
│   ├── complete_agent.py (agent logic)
│   └── requirements.txt   (dependencies)
│
├── frontend/             ← React app (port 3000)
│   ├── src/
│   │   ├── App.js        (main component)
│   │   └── App.css       (styling)
│   ├── public/
│   └── package.json
│
└── LOCALHOST_SETUP.md    (this file)
```

---

## 🚀 API Endpoints

All available at `http://localhost:5000`:

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/` | Health check |
| POST | `/search` | Search & apply to jobs |
| GET | `/stats` | Get statistics |
| GET | `/applications` | Get all applications |

---

## 🐛 Troubleshooting

### Issue: "Port 5000 already in use"
```bash
# Find process using port 5000
lsof -i :5000

# Kill it
kill -9 <PID>
```

### Issue: "Port 3000 already in use"
```bash
# Find process using port 3000
lsof -i :3000

# Kill it
kill -9 <PID>
```

### Issue: "pip: command not found"
Use `pip3` instead:
```bash
pip3 install -r requirements.txt
python3 app.py
```

### Issue: "npm: command not found"
Install Node.js from https://nodejs.org

### Issue: "Module not found: complete_agent"
Make sure all Python files are in `/backend`:
```bash
ls -la backend/
# Should show: app.py, complete_agent.py, job_searcher.py, etc.
```

### Issue: "CORS error" on frontend
Make sure backend is running:
```bash
curl http://localhost:5000/
# Should return JSON, not error
```

---

## 📝 Development Workflow

### 1. Make Changes to Backend
Edit `/backend/complete_agent.py` or `/backend/app.py`
→ Flask auto-reloads (in debug mode)
→ Refresh frontend to see changes

### 2. Make Changes to Frontend
Edit `/frontend/src/App.js` or `/frontend/src/App.css`
→ React auto-reloads (hot reload)
→ Changes appear instantly in browser

### 3. Test in Both Places
- **Backend:** `curl http://localhost:5000/search`
- **Frontend:** http://localhost:3000 (search form)

---

## 🎓 Learning Resources

Inside `/backend/`:
- `job_searcher.py` - Phase 1: Python fundamentals
- `multi_agent_orchestrator.py` - Phase 2: Multi-agent architecture
- `rag_semantic_matcher.py` - Phase 3: Semantic AI
- `complete_agent.py` - All phases integrated
- `app.py` - Flask API (your server)

Each file teaches different concepts. Read the comments!

---

## Next Steps

### Option 1: Explore Locally
- Modify job preferences in `complete_agent.py`
- Add new agents
- Experiment with embedding logic
- Build new features

### Option 2: Deploy to Cloud
When ready:
```bash
git add .
git commit -m "Local testing complete, ready for deployment"
git push
# Then deploy to Railway + Vercel (see DEPLOY_INSTRUCTIONS.md)
```

### Option 3: Add Database
Connect PostgreSQL to save applications:
```bash
pip install sqlalchemy psycopg2-binary
# Update app.py to save results
```

---

**Happy coding! Your AI agent is running locally! 🚀**

Questions? Check the code comments or run: `python3 complete_agent.py`
