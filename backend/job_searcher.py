"""
Phase 1: Job Searcher Agent
===========================

This is your FIRST agent. It searches for jobs based on your preferences.

By the end of Phase 1, you'll understand:
1. Python variables & data types
2. Functions (reusable blocks of code)
3. Classes (blueprints for objects)
4. API calls (getting data from the internet)
5. Loops & conditionals (decision-making)

Let's build!
"""

# ============================================
# LESSON 1: Variables & Data Types
# ============================================

# A VARIABLE is a container that holds a value
# Think of it like a labeled box

# String (text)
job_title = "Software Engineer"
location = "Remote"

# Integer (whole numbers)
salary_min = 100000
years_experience = 2

# Boolean (True or False)
is_remote = True
wants_startup = False

# List (multiple items, in order)
preferred_skills = ["Python", "React", "JavaScript"]

# Dictionary (key-value pairs, like labeled storage)
user_preferences = {
    "title": "Software Engineer",
    "location": "Remote",
    "salary_min": 100000,
    "skills": ["Python", "React"]
}

print("Your preferences:", user_preferences)


# ============================================
# LESSON 2: Functions (Reusable Code Blocks)
# ============================================

# A FUNCTION is code you can reuse by calling it by name
# Think: "I have a set of instructions, and I want to run them multiple times"

def greet_user(name):
    """
    Function: greet_user
    Input: name (a string)
    Output: prints a greeting
    """
    message = f"Hello, {name}! Welcome to the Job Agent."
    return message


# Call the function
greeting = greet_user("Padmavati")
print(greeting)


def filter_jobs_by_salary(jobs, min_salary):
    """
    Filter jobs that meet your salary requirement
    Input: jobs (list), min_salary (number)
    Output: filtered_jobs (list)
    """
    filtered = []
    for job in jobs:
        if job["salary"] >= min_salary:
            filtered.append(job)
    return filtered


# Mock jobs (pretend data from API)
mock_jobs = [
    {"title": "Junior Engineer", "salary": 90000, "company": "TechCorp"},
    {"title": "Senior Engineer", "salary": 150000, "company": "BigTech"},
    {"title": "Mid-level Engineer", "salary": 110000, "company": "StartupXYZ"}
]

# Use the function
matching_jobs = filter_jobs_by_salary(mock_jobs, 100000)
print("\nJobs matching your salary requirement:", matching_jobs)


# ============================================
# LESSON 3: Classes (Blueprints for Objects)
# ============================================

# A CLASS is a blueprint for creating objects
# Think: "I want to create multiple job-searcher agents, each with their own preferences"

class JobSearcher:
    """
    JobSearcher: An agent that searches for jobs

    Attributes:
    - preferences: what kind of jobs to search for
    - applications: list of jobs it has applied to
    """

    def __init__(self, preferences):
        """
        __init__: Initialize (create) a new JobSearcher
        This runs when you create a new instance

        Example:
        searcher = JobSearcher(preferences={...})
        """
        self.preferences = preferences
        self.applications = []  # Keep track of applied jobs
        print(f"✓ JobSearcher created with preferences: {preferences}")

    def search(self):
        """
        Search for jobs matching preferences
        Returns: list of matching jobs
        """
        print(f"\n🔍 Searching for {self.preferences['title']} in {self.preferences['location']}...")

        # TODO: Later, this will call real APIs (LinkedIn, Indeed)
        # For now, return mock data
        matching_jobs = []

        for job in mock_jobs:
            # Check if job matches your preference
            if (job["title"].lower() == self.preferences["title"].lower() or
                "Engineer" in job["title"]):
                matching_jobs.append(job)

        print(f"Found {len(matching_jobs)} matching jobs")
        return matching_jobs

    def apply(self, job):
        """
        Apply to a job
        """
        print(f"📝 Applying to {job['title']} at {job['company']}...")
        self.applications.append(job)
        return f"Applied to {job['title']}"

    def get_applications(self):
        """
        Get all applications you've made
        """
        return self.applications

    def count_applications(self):
        """
        Count total applications you've made
        Returns: number of applications
        """
        return len(self.applications)

    def filter_by_company(self, company_name):
        """
        Filter applications by company name
        Input: company_name (string)
        Output: list of applications from that company
        """
        matching = []
        for app in self.applications:
            if app["company"].lower() == company_name.lower():
                matching.append(app)
        return matching


# ============================================
# LESSON 4: Putting It All Together
# ============================================

# Create a JobSearcher instance (an actual searcher object)
preferences = {
    "title": "Software Engineer",
    "location": "Remote",
    "salary_min": 100000
}

searcher = JobSearcher(preferences)

# Search for jobs
jobs = searcher.search()

# Apply to matching jobs
for job in jobs:
    result = searcher.apply(job)
    print(f"  → {result}")

# Check your applications
print(f"\nTotal applications: {len(searcher.get_applications())}")


# ============================================
# LESSON 5: Loops & Conditionals
# ============================================

# FOR LOOP: Repeat code for each item in a list
print("\n--- Job Details ---")
for job in jobs:
    # CONDITIONAL: Make a decision based on data
    if job["salary"] >= 120000:
        status = "High Paying ✓"
    elif job["salary"] >= 100000:
        status = "Good Salary ✓"
    else:
        status = "Below your minimum"

    print(f"• {job['title']} at {job['company']} - ${job['salary']:,} - {status}")


# ============================================
# YOUR TURN: Challenges
# ============================================

# CHALLENGE 1: count_applications() method
print("\n--- CHALLENGE 1: Count Applications ---")
print(f"First searcher total applications: {searcher.count_applications()}")


# CHALLENGE 2: Create another JobSearcher with different preferences
print("\n--- CHALLENGE 2: Second Searcher ---")
preferences2 = {
    "title": "Data Scientist",
    "location": "San Francisco",
    "salary_min": 120000
}

searcher2 = JobSearcher(preferences2)
jobs2 = searcher2.search()

for job in jobs2:
    result = searcher2.apply(job)
    print(f"  → {result}")

print(f"Second searcher total applications: {searcher2.count_applications()}")


# CHALLENGE 3: filter_by_company() method
print("\n--- CHALLENGE 3: Filter by Company ---")
bigtechapps = searcher.filter_by_company("BigTech")
print(f"Applications at BigTech: {bigtechapps}")

techcorpapps = searcher.filter_by_company("TechCorp")
print(f"Applications at TechCorp: {techcorpapps}")

print("\n✅ Phase 1 Lesson Complete!")
print("Next: Phase 2 - Multi-Agent Architecture (Searcher, Applier, Emailer agents)")

# CHALLENGE 1 SOLUTION: Second Orchestrator
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

print("\n📊 Comparison:")
print(f"Software Engineer: {result['applications_made']} applications")
print(f"Data Scientist: {result2['applications_made']} applications")