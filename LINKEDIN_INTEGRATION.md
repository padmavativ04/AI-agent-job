# 🔗 LinkedIn Integration Guide

Complete guide to integrate LinkedIn job scraping and auto-apply functionality.

---

## 📋 What You Can Do

### ✅ Current Implementation (MVP)
- ✅ Search for jobs on LinkedIn (via API)
- ✅ Prepare application data
- ✅ Auto-fill form fields
- ✅ Track required fields per job

### ⏳ Production Implementation (Phase 2)
- 🚀 Real-time job sync from LinkedIn
- 🚀 Automated form filling with resume
- 🚀 Auto-apply with browser automation
- 🚀 Track application status
- 🚀 Receive notifications

---

## 🚀 Phase 1: MVP Setup (Today)

### Step 1: Install Dependencies

```bash
cd "/Users/padmavativaidyanathan/Desktop/Claude code/AI-agent-job/backend"

pip install linkedin-scraper requests beautifulsoup4
```

### Step 2: Test LinkedIn Fetcher

```bash
python3 -c "
from linkedin_fetcher import LinkedInJobFetcher, LinkedInApplicationManager

# Search jobs
fetcher = LinkedInJobFetcher()
jobs = fetcher.search_jobs('Customer Success Manager', 'Canada', 5)

print(f'Found {len(jobs)} jobs')
for job in jobs:
    print(f'  - {job[\"title\"]} @ {job[\"company\"]}')

# Prepare application
user_data = {
    'full_name': 'Your Name',
    'email': 'your.email@example.com',
    'phone': '+1 (555) 123-4567',
    'resume_path': '/path/to/resume.pdf',
    'linkedin_url': 'https://linkedin.com/in/yourprofile'
}

manager = LinkedInApplicationManager(user_data)
for job in jobs[:1]:
    result = manager.apply_to_job(job)
    print(f'\n{result[\"message\"]}')
    print(f'Required fields: {result[\"required_fields\"]}')
"
```

### Step 3: Test API Endpoints

```bash
# Search LinkedIn jobs
curl -X POST http://localhost:5000/linkedin/search \
  -H "Content-Type: application/json" \
  -d '{
    "keywords": "Customer Success",
    "location": "Canada",
    "limit": 5
  }'

# Response:
# {
#   "status": "success",
#   "source": "LinkedIn",
#   "total_jobs": 3,
#   "jobs": [...]
# }
```

---

## 🔑 Phase 2: Production LinkedIn Integration

### Option A: LinkedIn Official API (Recommended)

1. **Get LinkedIn API Access**
   ```
   https://www.linkedin.com/developers/
   ```

2. **Create App**
   - App name: AI Job Agent
   - Redirect URL: http://localhost:5000/auth/linkedin/callback
   - Scopes: r_liteprofile, r_emailaddress

3. **Update Credentials**
   ```bash
   # Create .env file
   LINKEDIN_CLIENT_ID=your_client_id
   LINKEDIN_CLIENT_SECRET=your_client_secret
   LINKEDIN_REDIRECT_URI=http://localhost:5000/auth/linkedin/callback
   ```

4. **Install OAuth Library**
   ```bash
   pip install requests-oauthlib
   ```

### Option B: RapidAPI LinkedIn Scraper (Easier)

1. **Sign up for RapidAPI**
   ```
   https://rapidapi.com/
   ```

2. **Subscribe to LinkedIn Data API**
   ```
   https://rapidapi.com/nishanthana19/api/linkedin-data-api
   ```

3. **Get API Key**
   - Copy your API key from dashboard

4. **Add to .env**
   ```bash
   LINKEDIN_API_KEY=your_rapidapi_key
   ```

5. **Update linkedin_fetcher.py**
   ```python
   def _fetch_real_linkedin_jobs(self, keywords, location):
       """Fetch real jobs from RapidAPI LinkedIn"""
       headers = {
           "X-RapidAPI-Key": self.api_key,
           "X-RapidAPI-Host": "linkedin-data-api.p.rapidapi.com"
       }
       params = {
           "keywords": keywords,
           "locationId": location,  # Location ID from API
           "limit": 20
       }
       response = requests.get(
           "https://linkedin-data-api.p.rapidapi.com/search-jobs",
           headers=headers,
           params=params
       )
       return response.json()
   ```

---

## 📝 Phase 3: Resume Management

### Store User Resume

```bash
# Create resume directory
mkdir -p "/Users/padmavativaidyanathan/Desktop/Claude code/AI-agent-job/backend/resumes"

# Upload resume via API
curl -X POST http://localhost:5000/upload-resume \
  -F "resume=@/path/to/your/resume.pdf"
```

### Update API for Resume Upload

```python
# In app.py
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'resumes'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload-resume', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return jsonify({"error": "No resume file"}), 400
    
    file = request.files['resume']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    
    return jsonify({
        "status": "success",
        "resume_path": filepath,
        "filename": filename
    }), 200
```

---

## 🤖 Phase 4: Auto-Apply with Browser Automation

### Option A: Selenium (Robust)

```bash
pip install selenium webdriver-manager
```

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class LinkedInAutoApplier:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
    
    def login(self):
        """Login to LinkedIn"""
        self.driver.get("https://www.linkedin.com/login")
        
        # Enter email
        email_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        email_field.send_keys(self.email)
        
        # Enter password
        password_field = self.driver.find_element(By.ID, "password")
        password_field.send_keys(self.password)
        
        # Submit
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
    
    def apply_to_job(self, job_url, form_data):
        """Apply to a job"""
        self.driver.get(job_url)
        
        # Click Easy Apply button
        easy_apply = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Easy Apply')]"))
        )
        easy_apply.click()
        
        # Fill forms
        self._fill_forms(form_data)
    
    def _fill_forms(self, form_data):
        """Fill application forms"""
        # Find all input fields
        inputs = self.driver.find_elements(By.TAG_NAME, "input")
        
        for input_field in inputs:
            label = input_field.get_attribute("aria-label")
            if label and label in form_data:
                input_field.send_keys(form_data[label])
    
    def close(self):
        """Close browser"""
        self.driver.quit()

# Usage
applier = LinkedInAutoApplier("your_email@example.com", "your_password")
applier.login()
applier.apply_to_job(job_url, form_data)
applier.close()
```

### Option B: Puppeteer (Faster)

```bash
npm install puppeteer
```

```javascript
const puppeteer = require('puppeteer');

class LinkedInAutoApplier {
    async login(email, password) {
        this.browser = await puppeteer.launch();
        this.page = await this.browser.newPage();
        
        await this.page.goto('https://www.linkedin.com/login');
        
        // Fill login form
        await this.page.type('#username', email);
        await this.page.type('#password', password);
        await this.page.click('button[type="submit"]');
        
        await this.page.waitForNavigation();
    }
    
    async applyToJob(jobUrl, formData) {
        await this.page.goto(jobUrl);
        
        // Click Easy Apply
        await this.page.click('button:contains("Easy Apply")');
        
        // Fill forms
        for (let [field, value] of Object.entries(formData)) {
            await this.page.type(`input[aria-label="${field}"]`, value);
        }
        
        // Submit
        await this.page.click('button[type="submit"]');
    }
    
    async close() {
        await this.browser.close();
    }
}
```

---

## 🔒 Security & Best Practices

### Protect Credentials

```bash
# Create .env file
LINKEDIN_EMAIL=your_email@example.com
LINKEDIN_PASSWORD=your_password
LINKEDIN_CLIENT_ID=your_client_id
LINKEDIN_CLIENT_SECRET=your_client_secret

# Load in Python
from dotenv import load_dotenv
import os

load_dotenv()
email = os.getenv('LINKEDIN_EMAIL')
password = os.getenv('LINKEDIN_PASSWORD')
```

### Rate Limiting

```python
import time
from functools import wraps

def rate_limit(calls_per_minute=5):
    min_interval = 60 / calls_per_minute
    
    def decorator(func):
        last_called = [0.0]
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            if elapsed < min_interval:
                time.sleep(min_interval - elapsed)
            
            result = func(*args, **kwargs)
            last_called[0] = time.time()
            return result
        
        return wrapper
    return decorator

@rate_limit(calls_per_minute=10)
def apply_to_job(job):
    # Apply logic here
    pass
```

### Error Handling

```python
class LinkedInError(Exception):
    pass

class LoginError(LinkedInError):
    pass

class ApplicationError(LinkedInError):
    pass

# Usage
try:
    applier.login(email, password)
except LoginError as e:
    logger.error(f"Login failed: {e}")
except ApplicationError as e:
    logger.error(f"Application failed: {e}")
```

---

## 📊 Track Applications

### Create Application Log

```python
import json
from datetime import datetime

class ApplicationLogger:
    def __init__(self, log_file='applications.json'):
        self.log_file = log_file
        self.applications = self._load_log()
    
    def _load_log(self):
        try:
            with open(self.log_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def log_application(self, job, status, notes=''):
        """Log an application"""
        entry = {
            'job_id': job['id'],
            'company': job['company'],
            'title': job['title'],
            'status': status,  # 'applied', 'rejected', 'interview', etc
            'timestamp': datetime.now().isoformat(),
            'notes': notes
        }
        self.applications.append(entry)
        self._save_log()
    
    def _save_log(self):
        with open(self.log_file, 'w') as f:
            json.dump(self.applications, f, indent=2)
    
    def get_stats(self):
        """Get application statistics"""
        return {
            'total': len(self.applications),
            'applied': sum(1 for a in self.applications if a['status'] == 'applied'),
            'rejected': sum(1 for a in self.applications if a['status'] == 'rejected'),
            'interview': sum(1 for a in self.applications if a['status'] == 'interview'),
            'accepted': sum(1 for a in self.applications if a['status'] == 'accepted')
        }
```

---

## 🚀 Complete Example

```python
# main.py
from linkedin_fetcher import LinkedInJobFetcher, LinkedInApplicationManager
from selenium_applier import LinkedInAutoApplier
from application_logger import ApplicationLogger

# Setup
fetcher = LinkedInJobFetcher(api_key='your_key')
logger = ApplicationLogger()

# Search jobs
jobs = fetcher.search_jobs('Customer Success', 'Canada', limit=10)

# Prepare applications
user_data = {
    'full_name': 'Your Name',
    'email': 'your.email@example.com',
    'phone': '+1 (555) 123-4567',
    'resume_path': '/path/to/resume.pdf',
    'linkedin_url': 'https://linkedin.com/in/yourprofile'
}

manager = LinkedInApplicationManager(user_data)

# Auto-apply
applier = LinkedInAutoApplier('your_email@linkedin.com', 'your_password')
applier.login()

for job in jobs:
    try:
        # Prepare application
        app_data = manager.apply_to_job(job)
        
        # Auto-apply on LinkedIn
        applier.apply_to_job(job['job_url'], app_data['form_data'])
        
        # Log success
        logger.log_application(job, 'applied', 'Successfully applied')
        print(f"✅ Applied to {job['company']} - {job['title']}")
        
    except Exception as e:
        logger.log_application(job, 'error', str(e))
        print(f"❌ Failed to apply to {job['company']}: {e}")

applier.close()

# Show stats
stats = logger.get_stats()
print(f"\nStats: {stats}")
```

---

## 🔗 API Endpoints

### Search LinkedIn Jobs
```bash
POST /linkedin/search
{
    "keywords": "Customer Success Manager",
    "location": "Canada",
    "limit": 20
}
```

### Apply to Job
```bash
POST /linkedin/apply
{
    "job_id": "linkedin-1",
    "full_name": "Your Name",
    "email": "your.email@example.com",
    "phone": "+1 (555) 123-4567",
    "resume_path": "/path/to/resume.pdf",
    "cover_letter": "Cover letter text"
}
```

### Upload Resume
```bash
POST /upload-resume
Form Data:
    - resume: (file)
```

### Get Application Stats
```bash
GET /linkedin/stats
```

---

## 📈 Implementation Timeline

**Week 1:** MVP with mock LinkedIn data (✅ Today)
**Week 2:** RapidAPI LinkedIn integration
**Week 3:** Resume management & form filling
**Week 4:** Selenium auto-apply automation
**Week 5:** Application tracking & logging
**Week 6:** Production deployment

---

## ⚠️ LinkedIn Terms of Service

- ✅ Use official LinkedIn API when available
- ✅ Respect rate limiting
- ⚠️ Automated applications may violate ToS
- ⚠️ Store credentials securely
- ⚠️ Use headless browsers carefully
- ⚠️ Get user consent before automating

---

## 🆘 Troubleshooting

### "LinkedIn login failed"
- Check email/password
- Verify not rate-limited
- Check if 2FA enabled

### "Application timeout"
- Increase wait times
- Check network connection
- Verify job URL is valid

### "Form fields not found"
- LinkedIn UI changes frequently
- Update selectors
- Log page HTML for debugging

---

**Ready to integrate LinkedIn? Start with Phase 1 MVP, then scale to automation!** 🚀
