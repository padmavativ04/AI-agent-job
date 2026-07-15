"""
╔══════════════════════════════════════════════════════════════════╗
║     AI JOB APPLICATION AGENT - Complete System                  ║
║     Phases 1-3: Python Fundamentals + Multi-Agent + RAG         ║
╚══════════════════════════════════════════════════════════════════╝

FEATURES:
✅ Phase 1: Python fundamentals (variables, functions, classes)
✅ Phase 2: Multi-agent architecture (Searcher, Applier, Emailer)
✅ Phase 3: Semantic matching with RAG (AI-powered job matching)

AGENTS:
1. JobSearcher - Finds jobs matching your criteria
2. Applier - Applies to matched jobs
3. Emailer - Sends follow-up emails
4. ReportGenerator - Summarizes results
5. SemanticMatcher - AI-powered matching
6. Orchestrator - Coordinates all agents
"""

import math
from datetime import datetime


# ============================================
# PHASE 1: Core Python Concepts
# ============================================

# Variables & Data Types
COMPANY_DATABASE = {
    "saas_companies": ["Shopify", "Slack", "HubSpot", "Salesforce", "Zendesk"],
    "job_types": ["Customer Success", "Onboarding", "Implementation", "Project Manager"],
}

MIN_SALARY_CAD = 50000
SEARCH_LOCATION = "Canada"


# ============================================
# PHASE 2 & 3: Agent Classes
# ============================================

class JobSearcher:
    """
    Agent 1: Searches for jobs
    Responsibility: Find jobs matching criteria
    """

    def __init__(self, name="JobSearcher"):
        self.name = name
        self.search_count = 0
        self.job_database = [
            # Customer Success
            {"id": 1, "title": "Customer Success Manager", "salary": 65000, "company": "Shopify", "location": "Toronto, Canada", "type": "SaaS", "description": "Help customers succeed with our platform. Manage relationships, solve problems."},
            {"id": 2, "title": "Customer Success", "salary": 58000, "company": "Freshworks", "location": "Remote", "type": "SaaS", "description": "Support customers in their journey. Build relationships and drive adoption."},
            {"id": 3, "title": "Customer Success Manager", "salary": 70000, "company": "HubSpot", "location": "Vancouver, Canada", "type": "SaaS", "description": "Lead customer success initiatives. Manage accounts and drive retention."},

            # Customer Onboarding
            {"id": 4, "title": "Customer Onboarding Specialist", "salary": 52000, "company": "Slack", "location": "Remote", "type": "SaaS", "description": "Welcome new customers, implement solutions, ensure smooth onboarding."},
            {"id": 5, "title": "Customer Onboarding Manager", "salary": 62000, "company": "Atlassian", "location": "Toronto, Canada", "type": "SaaS", "description": "Oversee customer onboarding process. Train and support new users."},

            # Implementation Consultant
            {"id": 6, "title": "Implementation Consultant", "salary": 75000, "company": "Salesforce", "location": "Remote", "type": "SaaS", "description": "Deploy and customize CRM solutions. Technical problem-solving and consulting."},
            {"id": 7, "title": "Implementation Consultant", "salary": 68000, "company": "Zendesk", "location": "Vancouver, Canada", "type": "SaaS", "description": "Implement support solutions. Configure systems and provide training."},

            # Project Manager
            {"id": 8, "title": "Project Manager", "salary": 72000, "company": "Asana", "location": "Remote", "type": "SaaS", "description": "Lead projects, manage teams, deliver results. Coordinate across departments."},
            {"id": 9, "title": "Project Manager", "salary": 66000, "company": "Jira", "location": "Montreal, Canada", "type": "SaaS", "description": "Manage software projects. Ensure on-time delivery and quality."},

            # Solutions Consultant
            {"id": 10, "title": "Solutions Consultant", "salary": 80000, "company": "Stripe", "location": "Remote", "type": "SaaS", "description": "Advise clients on technical solutions. Consult on implementation strategy."},
            {"id": 11, "title": "Solutions Consultant", "salary": 73000, "company": "Intercom", "location": "Toronto, Canada", "type": "SaaS", "description": "Partner with customers. Design communication solutions."},

            # Tech Support
            {"id": 12, "title": "Tech Support Specialist", "salary": 50000, "company": "GitHub", "location": "Remote", "type": "SaaS", "description": "Provide technical support. Help developers solve problems."},
            {"id": 13, "title": "Tech Support Manager", "salary": 65000, "company": "Notion", "location": "Vancouver, Canada", "type": "SaaS", "description": "Lead support team. Ensure customer satisfaction and issue resolution."},
        ]
        print(f"✓ {self.name} initialized with {len(self.job_database)} jobs")

    def search(self, preferences):
        """Search for jobs matching user preferences"""
        self.search_count += 1
        titles = preferences.get('titles', [])
        salary_min = preferences.get('salary_min', 0)
        location = preferences.get('location', '')

        print(f"\n🔍 {self.name}: Searching for {len(titles)} roles...")

        matching = []
        for job in self.job_database:
            # Match by title
            title_match = any(title.lower() in job["title"].lower() for title in titles)

            # Match by salary
            salary_match = job.get("salary", 0) >= salary_min

            # Match by location
            location_match = ("remote" in location.lower() and "remote" in job["location"].lower()) or \
                           ("canada" in location.lower())

            if title_match and salary_match and location_match:
                matching.append(job)

        print(f"   ✓ Found {len(matching)} matching jobs")
        return matching


class Applier:
    """
    Agent 2: Applies to jobs
    Responsibility: Submit applications
    """

    def __init__(self, name="Applier"):
        self.name = name
        self.applications = []
        self.apply_count = 0

    def apply(self, jobs):
        """Apply to a list of jobs"""
        self.apply_count += 1
        print(f"\n📝 {self.name}: Applying to {len(jobs)} job(s)...")

        for job in jobs:
            application = {
                "job_id": job["id"],
                "job_title": job["title"],
                "company": job["company"],
                "salary": job["salary"],
                "status": "applied",
                "date": datetime.now().strftime("%Y-%m-%d")
            }
            self.applications.append(application)
            print(f"   ✓ Applied to {job['title']} at {job['company']}")

        return self.applications

    def get_applications(self):
        """Get all applications"""
        return self.applications


class Emailer:
    """
    Agent 3: Sends emails
    Responsibility: Send rejection follow-ups
    """

    def __init__(self, name="Emailer"):
        self.name = name
        self.emails_sent = []
        self.email_count = 0

    def send_rejection_followup(self, applications):
        """Send follow-up emails"""
        self.email_count += 1
        print(f"\n📧 {self.name}: Sending {len(applications)} follow-up emails...")

        for app in applications:
            email = {
                "to_company": app["company"],
                "subject": f"Feedback Request: {app['job_title']} Application",
                "body": f"Hi {app['company']}, could you provide feedback on my {app['job_title']} application?",
                "status": "sent",
                "date": datetime.now().strftime("%Y-%m-%d")
            }
            self.emails_sent.append(email)
            print(f"   ✓ Email to {app['company']}")

        return self.emails_sent


class SemanticMatcher:
    """
    Agent 4: Semantic matching (Phase 3 - RAG)
    Responsibility: AI-powered job matching
    """

    def __init__(self, name="SemanticMatcher"):
        self.name = name
        self.matches_scored = 0

    def create_embedding(self, text):
        """Convert text to embedding (simplified)"""
        keywords = {
            'customer': [0.8, 0.5, 0.2],
            'help': [0.6, 0.9, 0.1],
            'technical': [0.2, 0.1, 0.9],
            'problem': [0.3, 0.2, 0.8],
            'lead': [0.6, 0.8, 0.5],
            'solve': [0.3, 0.4, 0.9],
        }

        text_lower = text.lower()
        embedding = [0.0, 0.0, 0.0]

        for word, vec in keywords.items():
            if word in text_lower:
                embedding = [embedding[i] + vec[i] for i in range(3)]

        norm = math.sqrt(sum(x**2 for x in embedding)) or 1
        return [x / norm for x in embedding]

    def cosine_similarity(self, vec1, vec2):
        """Calculate similarity between vectors"""
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = math.sqrt(sum(x**2 for x in vec1)) or 1
        norm2 = math.sqrt(sum(x**2 for x in vec2)) or 1
        return dot_product / (norm1 * norm2)

    def score_jobs(self, jobs, user_goals):
        """Score jobs by semantic similarity to user goals"""
        self.matches_scored += 1
        print(f"\n🧠 {self.name}: Scoring jobs semantically...")

        goals_embedding = self.create_embedding(user_goals)
        scored = []

        for job in jobs:
            job_text = f"{job['title']} {job['description']}"
            job_embedding = self.create_embedding(job_text)

            score = self.cosine_similarity(goals_embedding, job_embedding)
            job['semantic_score'] = score
            scored.append(job)

        scored.sort(key=lambda x: x['semantic_score'], reverse=True)
        print(f"   ✓ Scored {len(scored)} jobs")
        return scored


class ReportGenerator:
    """
    Agent 5: Report generation
    Responsibility: Summarize results
    """

    def __init__(self, name="ReportGenerator"):
        self.name = name
        self.reports_generated = 0

    def generate(self, results):
        """Generate comprehensive report"""
        self.reports_generated += 1
        print(f"\n📄 {self.name}: Generating report...")

        total_apps = sum(len(r['applications']) for r in results)
        total_emails = sum(len(r['emails']) for r in results)

        print(f"""
╔═════════════════════════════════════════╗
║         JOB APPLICATION REPORT          ║
╚═════════════════════════════════════════╝

📊 RESULTS
├─ Total Jobs Found: {sum(len(r['jobs']) for r in results)}
├─ Total Applications: {total_apps}
├─ Total Emails Sent: {total_emails}
└─ Report Date: {datetime.now().strftime("%Y-%m-%d %H:%M")}

✅ Status: All jobs applied! Follow-ups sent!
        """)
        return True


class Orchestrator:
    """
    Agent 6: Orchestrator (Main Coordinator)
    Coordinates all agents to execute job search workflow
    """

    def __init__(self):
        self.searcher = JobSearcher()
        self.applier = Applier()
        self.emailer = Emailer()
        self.matcher = SemanticMatcher()
        self.reporter = ReportGenerator()
        print(f"\n✓ Orchestrator initialized with 5 agents")

    def run(self, preferences):
        """
        Execute complete workflow:
        1. Search for jobs
        2. Score by semantic match
        3. Apply to jobs
        4. Send follow-ups
        5. Generate report
        """
        print("\n" + "=" * 60)
        print("COMPLETE JOB APPLICATION WORKFLOW")
        print("=" * 60)

        # Step 1: Search
        jobs = self.searcher.search(preferences)

        if not jobs:
            print("\n❌ No matching jobs found!")
            return None

        # Step 2: Semantic scoring (Phase 3)
        user_goals = preferences.get('goals', 'Find a great job that matches my skills')
        scored_jobs = self.matcher.score_jobs(jobs, user_goals)

        # Step 3: Apply
        applications = self.applier.apply(scored_jobs)

        # Step 4: Send emails
        emails = self.emailer.send_rejection_followup(applications)

        # Step 5: Report
        results = [{
            'jobs': scored_jobs,
            'applications': applications,
            'emails': emails
        }]
        self.reporter.generate(results)

        return {
            'jobs': scored_jobs,
            'applications': applications,
            'emails': emails,
            'status': 'success'
        }


# ============================================
# MAIN EXECUTION
# ============================================

if __name__ == "__main__":
    print("\n" + "🤖" * 30)
    print("AI JOB APPLICATION AGENT - COMPLETE SYSTEM")
    print("🤖" * 30)

    # Create orchestrator
    orchestrator = Orchestrator()

    # Your job preferences
    preferences = {
        "titles": [
            "Customer Success",
            "Customer Onboarding",
            "Implementation Consultant",
            "Project Manager",
            "Solutions Consultant",
            "Tech Support"
        ],
        "location": "Canada",
        "salary_min": 50000,
        "goals": "I want to help customers succeed and solve technical problems. I love learning new technologies."
    }

    # Run the complete workflow
    result = orchestrator.run(preferences)

    # Print detailed results
    if result:
        print("\n" + "=" * 60)
        print("DETAILED APPLICATION RESULTS")
        print("=" * 60)

        print("\n📋 Top Opportunities (by semantic match):")
        for i, job in enumerate(result['jobs'][:5], 1):
            score_pct = int(job.get('semantic_score', 0) * 100)
            print(f"\n{i}. {job['title']} at {job['company']}")
            print(f"   💰 Salary: ${job['salary']:,} CAD")
            print(f"   📍 Location: {job['location']}")
            print(f"   🎯 Match: {score_pct}%")

        print("\n" + "=" * 60)
        print("STATISTICS")
        print("=" * 60)
        print(f"Jobs Searched: {orchestrator.searcher.search_count}")
        print(f"Jobs Applied: {len(result['applications'])}")
        print(f"Emails Sent: {len(result['emails'])}")
        print(f"Agent Reports Generated: {orchestrator.reporter.reports_generated}")

    print("\n✅ Workflow Complete!")
    print("\n" + "=" * 60)
    print("NEXT STEPS")
    print("=" * 60)
    print("""
✅ Phase 1: Python Fundamentals - COMPLETE
✅ Phase 2: Multi-Agent Architecture - COMPLETE
✅ Phase 3: Agentic RAG - COMPLETE

🚀 WHAT'S NEXT:
1. Phase 4: Safety & Evaluation (guardrails)
2. Phase 5: Voice Interface (speak to your agent)
3. Phase 6: Deployment (live website + GitHub)

📚 To continue learning:
- Explore Phase 4: python rag_semantic_matcher.py (safety features)
- Build frontend: npm install && npm start (React UI)
- Deploy: git push to GitHub
    """)
