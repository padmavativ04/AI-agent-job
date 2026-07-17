# 🎨 React Frontend Development Guide

Complete guide to understanding and extending the AI Job Agent React frontend.

---

## 📁 Project Structure

```
frontend/
├── public/
│   ├── index.html          ← Main HTML file
│   └── favicon.ico
│
├── src/
│   ├── components/         ← Reusable React components
│   │   ├── Header.js       (Site header with status)
│   │   ├── SearchForm.js   (Job search input form)
│   │   ├── JobCard.js      (Individual job display)
│   │   └── StatsCards.js   (Results statistics)
│   │
│   ├── styles/             ← CSS for components
│   │   ├── Header.css
│   │   ├── SearchForm.css
│   │   ├── JobCard.css
│   │   └── StatsCards.css
│   │
│   ├── App.js              ← Main app component
│   ├── App.css             ← Main styling
│   ├── index.css           ← Global styles
│   └── index.js            ← Entry point
│
├── package.json            ← Dependencies
├── package-lock.json
└── node_modules/           ← Installed packages

```

---

## 🚀 Quick Start

### Install Dependencies
```bash
cd frontend
npm install
```

### Start Development Server
```bash
npm start
```

Opens automatically at **http://localhost:3000**

### Build for Production
```bash
npm run build
```

Creates optimized build in `build/` folder

---

## 📦 Components Overview

### 1. Header Component
**File:** `src/components/Header.js`

Displays the app title and live status badge.

```jsx
<Header />
// Renders: 🤖 AI Job Agent | Live & Ready
```

**Features:**
- Sticky positioning (stays at top)
- Status badge with pulse animation
- Responsive design

---

### 2. SearchForm Component
**File:** `src/components/SearchForm.js`

Form for users to enter job search preferences.

```jsx
<SearchForm onSearch={handleSearch} loading={loading} />
```

**Props:**
- `onSearch(preferences)` - Callback when form submitted
- `loading` - Boolean to show loading state

**Input Fields:**
- Job titles (comma-separated)
- Location
- Minimum salary
- Career goals

---

### 3. JobCard Component
**File:** `src/components/JobCard.js`

Displays a single job opportunity.

```jsx
<JobCard job={job} />
```

**Props:**
- `job` - Job object with: id, title, company, salary, location, description, match_score

**Features:**
- Shows match score badge
- Displays salary formatted with commas
- Hover effects
- Action buttons (Apply, Learn More)

---

### 4. StatsCards Component
**File:** `src/components/StatsCards.js`

Shows summary statistics of search results.

```jsx
<StatsCards stats={results} />
```

**Props:**
- `stats` - Object with: total_jobs, total_applications, total_emails

**Features:**
- 3-card grid layout
- Color-coded cards with icons
- Responsive on mobile

---

## 🎨 Styling System

### Colors
```javascript
Primary: #667eea (Purple-blue)
Secondary: #764ba2 (Dark purple)
Success: #4caf50 (Green)
Error: #ff4c4c (Red)
Background: Gradient: 135deg, #667eea → #764ba2
White: #ffffff
Dark: #333333
Gray: #666666
Light Gray: #e0e0e0
```

### CSS Organization
Each component has its own CSS file in `src/styles/`:
- Keeps styles co-located with components
- Easy to modify and maintain
- Clean separation of concerns

### Responsive Breakpoints
```css
Mobile: < 480px
Tablet: 480px - 768px
Desktop: > 768px
```

---

## 🔄 Data Flow

```
User Input (SearchForm)
        ↓
App.js (handleSearch)
        ↓
axios.post() to Backend
        ↓
Backend processes (Python)
        ↓
Returns JSON results
        ↓
setResults() updates state
        ↓
Components re-render with data
        ↓
StatsCards + JobCard display results
```

---

## 💻 Key Code Examples

### Calling the API
```javascript
// In App.js
const handleSearch = async (preferences) => {
  const response = await axios.post(
    `${BACKEND_URL}/search`,
    preferences
  );
  setResults(response.data);
};
```

### Props Example
```javascript
// Parent Component (App.js)
<SearchForm onSearch={handleSearch} loading={loading} />

// Child Component (SearchForm.js)
function SearchForm({ onSearch, loading }) {
  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch(preferences);
  };
}
```

### State Management
```javascript
const [results, setResults] = useState(null);
const [loading, setLoading] = useState(false);
const [error, setError] = useState(null);
```

---

## 🛠️ Customization Guide

### Change Color Scheme

Edit `src/App.css` and component CSS files:

```css
/* Old */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
color: #667eea;

/* New - Example: Orange/Yellow */
background: linear-gradient(135deg, #ff9500 0%, #ff6b6b 100%);
color: #ff9500;
```

### Add a New Component

1. Create component file: `src/components/MyComponent.js`
2. Create styles: `src/styles/MyComponent.css`
3. Import in App.js: `import MyComponent from './components/MyComponent'`
4. Use in JSX: `<MyComponent />`

Example:

```javascript
// src/components/Footer.js
import React from 'react';
import '../styles/Footer.css';

function Footer() {
  return (
    <footer className="footer">
      <p>© 2024 AI Job Agent</p>
    </footer>
  );
}

export default Footer;
```

### Modify the Search Form

Edit `src/components/SearchForm.js`:

```javascript
// Add new input field
<div className="form-group">
  <label htmlFor="remote">Remote Only?</label>
  <input
    id="remote"
    type="checkbox"
    checked={preferences.remote}
    onChange={(e) =>
      setPreferences({ ...preferences, remote: e.target.checked })
    }
  />
</div>
```

### Add New Results Section

Edit `src/App.js`:

```javascript
// In the results section
{results && (
  <div className="new-section">
    <h2>📈 Analytics</h2>
    <p>Add custom results here</p>
  </div>
)}
```

---

## 📱 Responsive Design

### Mobile-First Approach

The design is mobile-first and scales up:

```css
/* Mobile - Base styles */
.component {
  width: 100%;
  padding: 20px;
}

/* Tablet and up */
@media (min-width: 768px) {
  .component {
    width: 50%;
    padding: 30px;
  }
}

/* Desktop and up */
@media (min-width: 1200px) {
  .component {
    width: 33.33%;
  }
}
```

---

## 🐛 Common Issues & Solutions

### Issue: "Cannot find module 'axios'"
```bash
npm install axios
```

### Issue: "Port 3000 already in use"
```bash
# Find and kill the process
lsof -i :3000
kill -9 <PID>

# Or use different port
PORT=3001 npm start
```

### Issue: "Backend connection error"
Make sure:
1. Backend is running: `python3 app.py`
2. Backend URL is correct in App.js
3. CORS is enabled on backend

### Issue: "Styles not applying"
Check:
1. CSS file is imported: `import '../styles/MyComponent.css'`
2. Class names match: `className="my-class"` → `.my-class {}`
3. Specificity - use more specific selectors if needed

---

## 🎯 Testing Locally

### Test 1: Form Submission
1. Enter job titles
2. Click "Search & Apply"
3. Should show loading spinner
4. Results should display

### Test 2: Responsive Design
```bash
# Open DevTools in browser (F12)
# Click device toolbar icon
# Test on Mobile, Tablet, Desktop
```

### Test 3: API Connection
```javascript
// In browser console
fetch('http://localhost:5000/')
  .then(r => r.json())
  .then(d => console.log(d))
```

---

## 📚 Learning Resources

### React Concepts Used
- **Components:** Reusable UI pieces
- **Props:** Pass data to components
- **State:** Component data that changes
- **JSX:** HTML-like syntax in JavaScript
- **Hooks:** useState for state management
- **Conditional Rendering:** Show/hide elements

### Next Steps to Learn
1. **useState Hook:** Managing component state
2. **useEffect Hook:** Side effects and API calls
3. **Context API:** Global state management
4. **React Router:** Multiple pages
5. **Redux:** Complex state management

### Official Docs
- React: https://react.dev
- axios: https://axios-http.com
- CSS-in-JS: https://styled-components.com

---

## 🚀 Deployment

### Deploy to Vercel (Recommended)

```bash
npm install -g vercel
vercel
```

Follow prompts and your app goes live!

### Deploy to Netlify

```bash
npm run build
# Drag 'build' folder to netlify.com
```

### Deploy to GitHub Pages

Edit `package.json`:
```json
"homepage": "https://yourusername.github.io/AI-agent-job"
```

Deploy:
```bash
npm install gh-pages --save-dev
npm run build
npm run deploy
```

---

## 📝 Best Practices

### Component Organization
✅ One component per file
✅ Component name matches filename (PascalCase)
✅ Styles co-located with components
✅ Props clearly defined

### CSS Best Practices
✅ Use CSS Grid for layouts
✅ Use Flexbox for alignment
✅ Mobile-first responsive design
✅ Meaningful class names
✅ Avoid inline styles

### Performance
✅ Lazy load components if needed
✅ Memoize expensive components
✅ Avoid unnecessary re-renders
✅ Optimize images

### Accessibility
✅ Use semantic HTML
✅ Add alt text to images
✅ Use proper heading hierarchy
✅ Ensure color contrast

---

## 🤝 Contributing

Want to add features?

1. Create a new branch: `git checkout -b feature-name`
2. Make changes
3. Test thoroughly
4. Commit: `git commit -m "Add feature-name"`
5. Push: `git push origin feature-name`
6. Create Pull Request

---

## 📞 Support

- Check component comments in code
- Look at existing components for examples
- Test in browser DevTools
- Check React documentation

---

**Happy coding! 🚀**
