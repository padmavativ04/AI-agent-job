# 🔧 Troubleshooting Guide - Backend Connection Error

## ⚠️ Problem: "Connection Error: Make sure backend is running at http://localhost:5000"

Even though the backend appears to be running, the React frontend can't connect to it.

---

## ✅ Solution (Follow These Steps)

### Step 1: Kill All Old Processes
```bash
# Kill everything on port 5000
lsof -i :5000 | grep LISTEN | awk '{print $2}' | xargs kill -9 2>/dev/null || true

# Kill everything on port 3000
lsof -i :3000 | grep LISTEN | awk '{print $2}' | xargs kill -9 2>/dev/null || true

# Kill any python processes
pkill -f "python3 app.py" || true
pkill -f "npm start" || true

# Wait a moment
sleep 3

echo "✅ All processes killed"
```

---

### Step 2: Install Missing Dependencies
```bash
# Go to backend
cd "/Users/padmavativaidyanathan/Desktop/Claude code/AI-agent-job/backend"

# Install all requirements (including flask-cors)
pip install -r requirements.txt

# Verify flask-cors is installed
pip install flask-cors

echo "✅ Dependencies installed"
```

---

### Step 3: Start Backend (Terminal 1)
**Open a NEW terminal and run:**

```bash
cd "/Users/padmavativaidyanathan/Desktop/Claude code/AI-agent-job/backend"
python3 app.py
```

**Wait for this message:**
```
✓ JobSearcher initialized with 13 jobs
✓ Orchestrator initialized with 5 agents
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

✅ **Copy this message screenshot or text - it proves backend is running!**

---

### Step 4: Start Frontend (Terminal 2)
**Open ANOTHER NEW terminal and run:**

```bash
cd "/Users/padmavativaidyanathan/Desktop/Claude code/AI-agent-job/frontend"
npm start
```

**Wait for:**
```
Compiled successfully!
You can now view the app in your browser.
  Local: http://localhost:3000
```

---

### Step 5: Refresh Browser
1. Go to **http://localhost:3000**
2. Press **F5** or **CTRL+R** to refresh
3. Wait 2-3 seconds
4. You should see **✅ Backend Connected** message

---

## 🔍 Verification Checklist

- [ ] Terminal 1 shows: `Running on http://127.0.0.1:5000`
- [ ] Terminal 2 shows: `Local: http://localhost:3000`
- [ ] Browser shows no error banner
- [ ] Browser shows search form
- [ ] Browser shows "✅ Backend Connected" (optional)

---

## 🛠️ If Still Not Working

### Check Port 5000
```bash
# See what's using port 5000
lsof -i :5000

# If something shows up, kill it
lsof -i :5000 | grep LISTEN | awk '{print $2}' | xargs kill -9
```

### Check Backend Directly
```bash
# Test backend health check
curl http://localhost:5000/

# You should see JSON response like:
# {"status":"online","service":"AI Job Application Agent",...}
```

### Check Network
```bash
# Make sure localhost resolves
ping localhost

# Make sure port is accessible
nc -zv localhost 5000
```

### Check Python Installation
```bash
# Verify Python
python3 --version

# Verify pip
pip3 --version

# Verify flask-cors is installed
pip3 show flask-cors
```

---

## 🚨 Common Issues & Fixes

### Issue 1: "Address already in use"
```bash
# Find process on port 5000
lsof -i :5000

# Kill it
kill -9 <PID>

# Then start backend again
python3 app.py
```

### Issue 2: "ModuleNotFoundError: No module named 'flask_cors'"
```bash
# Install missing dependency
pip install flask-cors

# Then restart backend
python3 app.py
```

### Issue 3: Backend shows errors
```bash
# Make sure you're in the right directory
pwd
# Should show: .../AI-agent-job/backend

# Check app.py exists
ls -la app.py

# Try starting again
python3 app.py
```

### Issue 4: Browser still shows error after all steps
1. Close browser completely
2. Open new browser window
3. Clear cache: CTRL+SHIFT+Delete
4. Go to http://localhost:3000
5. Refresh page

---

## 📋 Complete Fresh Start

If nothing works, do a **complete restart**:

```bash
# Kill all processes
pkill -f "python3"
pkill -f "npm"
sleep 3

# Terminal 1: Start backend
cd "/Users/padmavativaidyanathan/Desktop/Claude code/AI-agent-job/backend"
pip install -r requirements.txt
python3 app.py

# In another terminal (Terminal 2): Start frontend
cd "/Users/padmavativaidyanathan/Desktop/Claude code/AI-agent-job/frontend"
npm install
npm start

# Browser: Go to http://localhost:3000
# Refresh with F5
```

---

## 🎯 What's Happening

1. **Backend** (Flask) runs on `http://localhost:5000`
   - Processes job searches
   - Returns JSON results
   - Has CORS enabled to allow frontend access

2. **Frontend** (React) runs on `http://localhost:3000`
   - Shows search form
   - Calls backend API
   - Displays results

3. **Connection** happens via HTTP
   - Frontend → HTTP request → Backend
   - Backend processes → Returns JSON
   - Frontend displays results

---

## 📝 Before/After

### Before Connection Error
```
Frontend (localhost:3000) tries to call Backend (localhost:5000)
                              ↓
                         FAILS ❌
                 (CORS error or timeout)
                              ↓
                    Error displayed to user
```

### After Fix
```
Frontend (localhost:3000) tries to call Backend (localhost:5000)
                              ↓
                        SUCCESS ✅
                   (CORS enabled, flask-cors installed)
                              ↓
                    Results displayed to user
```

---

## 💡 Pro Tips

1. **Keep terminals visible** - See all messages
2. **Don't close terminals** - Backend/Frontend must keep running
3. **Refresh browser** - After starting frontend
4. **Check console** - Browser F12 → Console tab for errors
5. **Check network** - Browser F12 → Network tab to see API calls

---

## 🆘 Still Stuck?

1. **Take a screenshot** of Terminal 1 and Terminal 2
2. **Copy the error message** from browser
3. **Check browser console** (F12 → Console)
4. **Run this debug script:**

```bash
cd "/Users/padmavativaidyanathan/Desktop/Claude code/AI-agent-job"

# Check backend
echo "=== BACKEND CHECK ==="
cd backend
python3 -c "from app import app; print('✅ Backend imports OK')"
pip show flask-cors

# Check frontend
echo -e "\n=== FRONTEND CHECK ==="
cd ../frontend
npm list react react-dom axios

# Check ports
echo -e "\n=== PORT CHECK ==="
lsof -i :5000 | head -5
lsof -i :3000 | head -5
```

---

**You've got this! Follow the steps above and your AI Job Agent will be running! 🚀**
