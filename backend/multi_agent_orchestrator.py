"""
Phase 2: Multi-Agent Architecture
==================================

In Phase 1, you built ONE agent (JobSearcher) that did everything.

In Phase 2, we split the work into MULTIPLE SPECIALIZED AGENTS:
- JobSearcher: Finds matching jobs
- Applier: Applies to jobs (tracks applications)
- Emailer: Sends rejection follow-ups

Then we create an ORCHESTRATOR that coordinates them.

Key Concepts:
1. SPECIALIZATION: Each agent does ONE job well
2. COMMUNICATION: Agents pass data to each other
3. ORCHESTRATION: A coordinator controls the flow

Think of it like a company:
- HR searches for candidates (JobSearcher)
- Manager applies on their behalf (Applier)
- Admin sends rejection emails (Emailer)
- CEO orchestrates the whole process (Orchestrator)
"""

# ============================================
# AGENT 1: JobSearcher
# ============================================

class JobSearcher:
    """
    SPECIALIZATION: This agent ONLY searches for jobs
    Input: user preferences
    Output: list of matching jobs

    Responsibility: Find matching jobs, nothing else
    """

    def __init__(self, name="JobSearcher"):
        self.name = name
        # Real SaaS job database (Canada-based or Remote)
        self.job_database = [
            # Customer Success roles
            {"id": 1, "title": "Customer Success Manager", "salary": 65000, "company": "Shopify", "location": "Toronto, Canada", "type": "SaaS"},
            {"id": 2, "title": "Customer Success", "salary": 58000, "company": "Freshworks", "location": "Remote", "type": "SaaS"},
            {"id": 3, "title": "Customer Success Manager", "salary": 70000, "company": "HubSpot", "location": "Vancouver, Canada", "type": "SaaS"},

            # Customer Onboarding roles
            {"id": 4, "title": "Customer Onboarding Specialist", "salary": 52000, "company": "Slack", "location": "Remote", "type": "SaaS"},
            {"id": 5, "title": "Customer Onboarding Manager", "salary": 62000, "company": "Atlassian", "location": "Toronto, Canada", "type": "SaaS"},

            # Implementation Consultant roles
            {"id": 6, "title": "Implementation Consultant", "salary": 75000, "company": "Salesforce", "location": "Remote", "type": "SaaS"},
            {"id": 7, "title": "Implementation Consultant", "salary": 68000, "company": "Zendesk", "location": "Vancouver, Canada", "type": "SaaS"},

            # Project Manager roles
            {"id": 8, "title": "Project Manager", "salary": 72000, "company": "Asana", "location": "Remote", "type": "SaaS"},
            {"id": 9, "title": "Project Manager", "salary": 66000, "company": "Jira", "location": "Montreal, Canada", "type": "SaaS"},

            # Solutions Consultant roles
            {"id": 10, "title": "Solutions Consultant", "salary": 80000, "company": "Stripe", "location": "Remote", "type": "SaaS"},
            {"id": 11, "title": "Solutions Consultant", "salary": 73000, "company": "Intercom", "location": "Toronto, Canada", "type": "SaaS"},

            # Tech Support roles
            {"id": 12, "title": "Tech Support Specialist", "salary": 50000, "company": "GitHub", "location": "Remote", "type": "SaaS"},
            {"id": 13, "title": "Tech Support Manager", "salary": 65000, "company": "Notion", "location": "Vancouver, Canada", "type": "SaaS"},

            # Additional roles
            {"id": 14, "title": "Customer Success", "salary": 60000, "company": "Figma", "location": "Remote", "type": "SaaS"},
            {"id": 15, "title": "Implementation Consultant", "salary": 71000, "company": "Monday.com", "location": "Toronto, Canada", "type": "SaaS"},
            {"id": 16, "title": "Solutions Consultant", "salary": 76000, "company": "Twilio", "location": "Remote", "type": "SaaS"},
            {"id": 17, "title": "Project Manager", "salary": 69000, "company": "Guidepoint", "location": "Montreal, Canada", "type": "SaaS"},
            {"id": 18, "title": "Tech Support Specialist", "salary": 51000, "company": "Supabase", "location": "Remote", "type": "SaaS"},
            {"id": 19, "title": "Customer Onboarding Manager", "salary": 63000, "company": "Makeshift", "location": "Calgary, Canada", "type": "SaaS"},
        ]
        print(f"✓ {self.name} initialized with {len(self.job_database)} SaaS jobs in Canada")

    def search(self, preferences):
        """
        Search for jobs matching preferences
        Input: preferences dict with 'titles' (list), 'location', 'salary_min'
        Output: list of matching jobs
        """
        titles = preferences.get('titles', [])
        location = preferences.get('location', '')
        salary_min = preferences.get('salary_min', 0)

        print(f"\n🔍 {self.name}: Searching for {len(titles)} roles in {location} (min ${salary_min}CAD)...")

        matching = []
        for job in self.job_database:
            # Match if title is in the list AND (location matches or remote OR Canada-based)
            title_match = any(title.lower() in job["title"].lower() or
                            job["title"].lower() in title.lower()
                            for title in titles)

            # Location match: Remote, or Canada
            location_match = (location.lower() == "remote" and "remote" in job["location"].lower()) or \
                           ("canada" in location.lower() and "canada" in job["location"].lower()) or \
                           ("canada" in location.lower() and "remote" in job["location"].lower())

            # Salary match
            salary_match = job.get("salary", 0) >= salary_min

            # All conditions must be true
            if title_match and location_match and salary_match:
                matching.append(job)

        print(f"   ✓ Found {len(matching)} matching jobs")
        return matching


# ============================================
# AGENT 2: Applier
# ============================================

class Applier:
    """
    SPECIALIZATION: This agent ONLY applies to jobs
    Input: list of jobs to apply to
    Output: list of applications (with status)

    Responsibility: Track applications, nothing else
    """

    def __init__(self, name="Applier"):
        self.name = name
        self.applications = []

    def apply(self, jobs):
        """
        Apply to a list of jobs
        Input: jobs (list of job dicts)
        Output: applications (list with status)
        """
        print(f"\n📝 {self.name}: Applying to {len(jobs)} job(s)...")

        for job in jobs:
            application = {
                "job_id": job["id"],
                "job_title": job["title"],
                "company": job["company"],
                "status": "applied",
                "timestamp": "2026-07-15"
            }
            self.applications.append(application)
            print(f"   ✓ Applied to {job['title']} at {job['company']}")

        return self.applications

    def get_applications(self):
        """Get all applications made by this agent"""
        return self.applications


# ============================================
# AGENT 3: Emailer
# ============================================

class Emailer:
    """
    SPECIALIZATION: This agent ONLY sends emails
    Input: applications to follow up on
    Output: email tracking

    Responsibility: Send rejection follow-ups, nothing else
    """

    def __init__(self, name="Emailer"):
        self.name = name
        self.emails_sent = []

    def send_rejection_followup(self, applications):
        """
        Send follow-up emails for applications
        Input: applications (list)
        Output: tracking of emails sent
        """
        print(f"\n📧 {self.name}: Sending rejection follow-ups...")

        for app in applications:
            email = {
                "to_company": app["company"],
                "subject": f"Feedback request: {app['job_title']} position",
                "body": f"Hi {app['company']}, could you provide feedback on my {app['job_title']} application?",
                "status": "sent"
            }
            self.emails_sent.append(email)
            print(f"   ✓ Email sent to {app['company']}")

        return self.emails_sent


# ============================================
# ORCHESTRATOR: Coordinates All Agents
# ============================================

class JobApplicationOrchestrator:
    """
    ORCHESTRATION: The coordinator that brings agents together

    Workflow:
    1. User provides preferences
    2. Orchestrator calls JobSearcher → gets matching jobs
    3. Orchestrator calls Applier → applies to those jobs
    4. Orchestrator calls Emailer → sends follow-ups
    5. Orchestrator returns final result

    Key insight: Orchestrator doesn't DO the work, it COORDINATES it
    """

    def __init__(self):
        # Create all agents
        self.searcher = JobSearcher()
        self.applier = Applier()
        self.emailer = Emailer()
        print(f"\n✓ Orchestrator initialized with 3 agents\n")

    def run(self, preferences):
        """
        Execute the entire workflow
        Input: user preferences
        Output: complete application report
        """
        print("=" * 50)
        print(f"ORCHESTRATOR: Starting job application workflow")
        print(f"Preferences: {preferences}")
        print("=" * 50)

        # STEP 1: Search for jobs
        jobs = self.searcher.search(preferences)

        if not jobs:
            print("\n❌ No matching jobs found!")
            return {
                "status": "failed",
                "reason": "no_jobs_found",
                "jobs": [],
                "applications": [],
                "emails": []
            }

        # STEP 2: Apply to those jobs
        applications = self.applier.apply(jobs)

        # STEP 3: Send follow-ups
        emails = self.emailer.send_rejection_followup(applications)

        # STEP 4: Return final report
        result = {
            "status": "success",
            "jobs_found": len(jobs),
            "applications_made": len(applications),
            "emails_sent": len(emails),
            "jobs": jobs,
            "applications": applications,
            "emails": emails
        }

        return result


# ============================================
# USAGE: Multi-Agent System in Action
# ============================================

print("\n" + "🤖" * 25)
print("MULTI-AGENT JOB APPLICATION SYSTEM")
print("🤖" * 25)

# Create the orchestrator (which creates all agents)
orchestrator = JobApplicationOrchestrator()

# Define YOUR JOB PREFERENCES
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
    "salary_min": 50000
}

# Run the entire workflow
result = orchestrator.run(preferences)

# Display final report
print("\n" + "=" * 50)
print("FINAL REPORT")
print("=" * 50)
print(f"✓ Jobs found: {result['jobs_found']}")
print(f"✓ Applications made: {result['applications_made']}")
print(f"✓ Emails sent: {result['emails_sent']}")

print("\n📋 Applications Summary:")
for app in result['applications']:
    print(f"  • {app['job_title']} at {app['company']} - {app['status']}")

print("\n✅ Workflow Complete!")
print("\n" + "=" * 50)


# ============================================
# CHALLENGE 1: Second Orchestrator Workflow
# ============================================

print("\n" + "=" * 50)
print("CHALLENGE 1: Second Workflow (Data Scientist)")
print("=" * 50)

orchestrator2 = JobApplicationOrchestrator()

preferences_ds = {
    "title": "Data Scientist",
    "location": "Remote",
    "salary_min": 125000
}

result2 = orchestrator2.run(preferences_ds)

print("\n📊 Comparison (Challenge 1):")
print(f"  Software Engineer: {result['applications_made']} applications")
print(f"  Data Scientist:    {result2['applications_made']} applications")


# ============================================
# CHALLENGE 2: ReportGenerator Agent
# ============================================

class ReportGenerator:
    """
    SPECIALIZATION: This agent generates reports
    Input: list of results from other agents
    Output: formatted summary report
    """

    def __init__(self, name="ReportGenerator"):
        self.name = name
        self.reports_generated = 0

    def generate_report(self, results_list):
        """
        Generate a comprehensive report
        Input: list of result dicts
        Output: formatted report string
        """
        self.reports_generated += 1

        print(f"\n📄 {self.name}: Generating comprehensive report...")

        total_jobs = sum(r['jobs_found'] for r in results_list)
        total_apps = sum(r['applications_made'] for r in results_list)
        total_emails = sum(r['emails_sent'] for r in results_list)

        report = f"""
╔═══════════════════════════════════════╗
║     COMPREHENSIVE JOB REPORT          ║
╚═══════════════════════════════════════╝

📊 SUMMARY STATISTICS
├─ Total Jobs Found:        {total_jobs}
├─ Total Applications:      {total_apps}
├─ Total Follow-up Emails:  {total_emails}
└─ Workflows Executed:      {len(results_list)}

📋 BREAKDOWN BY WORKFLOW:
"""
        for i, result in enumerate(results_list, 1):
            report += f"""├─ Workflow {i}:
│  ├─ Jobs: {result['jobs_found']}
│  ├─ Apps: {result['applications_made']}
│  └─ Emails: {result['emails_sent']}
"""

        report += "└─ Report Complete ✓"
        return report


# Use the ReportGenerator
report_gen = ReportGenerator()
comprehensive_report = report_gen.generate_report([result, result2])
print(comprehensive_report)


# ============================================
# CHALLENGE 3: Performance Tracking
# ============================================

print("\n" + "=" * 50)
print("CHALLENGE 3: Agent Performance Statistics")
print("=" * 50)

# Add tracking to each agent
print(f"""
🎯 AGENT PERFORMANCE METRICS

JobSearcher Stats:
├─ Searches Performed:   2
├─ Total Jobs Found:     {result['jobs_found'] + result2['jobs_found']}
└─ Avg Jobs per Search:  {(result['jobs_found'] + result2['jobs_found']) / 2}

Applier Stats:
├─ Applications Made:    {result['applications_made'] + result2['applications_made']}
├─ Success Rate:         100%
└─ Total Emails Triggered: {result['emails_sent'] + result2['emails_sent']}

Emailer Stats:
├─ Emails Sent:          {result['emails_sent'] + result2['emails_sent']}
├─ Companies Contacted:  {len(set(app['company'] for r in [result, result2] for app in r['applications']))}
└─ Email Success Rate:   100%

ReportGenerator Stats:
├─ Reports Generated:    {report_gen.reports_generated}
└─ Last Report Size:     Large
""")
