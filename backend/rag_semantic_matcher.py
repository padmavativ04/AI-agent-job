"""
Phase 3: Agentic RAG & Semantic Matching
=========================================

In Phase 2, your agent matched jobs by KEYWORDS:
  ❌ "Customer Success" → Must match exactly
  ❌ Misses nuanced matches
  ❌ Can't understand context

In Phase 3, your agent matches by MEANING:
  ✅ "I want to help customers" → Finds Customer Success, Onboarding, Support
  ✅ "I like problem-solving" → Finds Technical roles + Solutions roles
  ✅ "Remote work is important" → Prioritizes Remote jobs
  ✅ "I want growth" → Ranks by company potential

KEY CONCEPTS:
1. EMBEDDINGS: Convert text → numbers (vectors)
2. SIMILARITY: Find similar jobs by comparing vectors
3. RETRIEVAL: Get the best matching jobs
4. GENERATION: Generate explanations why jobs match

Think of it like this:
- Phase 1 & 2: "Find jobs with exact keywords"
- Phase 3: "Find jobs that feel like a good fit based on meaning"

WHY IT MATTERS:
- More accurate matches
- Understand career goals, not just keywords
- Find hidden opportunities
- Better job recommendations
"""

# ============================================
# LESSON: Embeddings & Vectors
# ============================================

print("""
╔════════════════════════════════════════════╗
║         WHAT ARE EMBEDDINGS?              ║
╚════════════════════════════════════════════╝

Embedding = Converting text into NUMBERS (a vector)

Example:
  "I love helping customers"
    ↓ (Embedding model)
  [0.234, -0.156, 0.891, 0.045, ...]  (300-dimensional vector)

Why?
  - Computers understand numbers better than text
  - Similar texts have similar embeddings
  - We can calculate distance between embeddings

Real-world analogy:
  - Star map: Each person is a point in space
  - Closer points = more similar people
  - Same concept: Embeddings create a "job space"
    where similar jobs are close together
""")


# ============================================
# SIMPLE EMBEDDING SIMULATOR
# ============================================

import math

def simple_embedding(text):
    """
    Simulate creating an embedding
    (In real life, we use ML models like sentence-transformers)

    For demo: Convert text to a simple vector based on keywords
    """
    keywords = {
        'customer': [0.8, 0.5, 0.2],
        'help': [0.6, 0.9, 0.1],
        'technical': [0.2, 0.1, 0.9],
        'problem': [0.3, 0.2, 0.8],
        'remote': [0.7, 0.7, 0.3],
        'lead': [0.6, 0.8, 0.5],
        'manage': [0.7, 0.8, 0.4],
        'solve': [0.3, 0.4, 0.9],
        'implement': [0.4, 0.5, 0.8],
        'consult': [0.6, 0.7, 0.6],
    }

    text_lower = text.lower()
    embedding = [0.0, 0.0, 0.0]

    # Sum embeddings of all keywords found
    for word, vec in keywords.items():
        if word in text_lower:
            embedding = [embedding[i] + vec[i] for i in range(3)]

    # Normalize
    norm = math.sqrt(sum(x**2 for x in embedding)) or 1
    embedding = [x / norm for x in embedding]

    return embedding


def cosine_similarity(vec1, vec2):
    """
    Calculate similarity between two vectors (0 to 1)
    1.0 = identical
    0.0 = completely different
    """
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = math.sqrt(sum(x**2 for x in vec1)) or 1
    norm2 = math.sqrt(sum(x**2 for x in vec2)) or 1
    return dot_product / (norm1 * norm2)


# ============================================
# AGENT 1: RAG Router (NEW)
# ============================================

class RAGRouter:
    """
    SPECIALIZATION: Decides HOW to search for jobs

    Routes to:
    - Semantic search (understanding meaning)
    - Keyword search (exact matches)
    - Hybrid search (both)
    """

    def __init__(self, name="RAGRouter"):
        self.name = name
        self.routing_decisions = []

    def analyze_preferences(self, preferences):
        """
        Analyze user preferences to decide search strategy
        """
        titles = " ".join(preferences.get('titles', []))
        goals = preferences.get('goals', '')

        # Create embeddings
        titles_embedding = simple_embedding(titles)
        goals_embedding = simple_embedding(goals) if goals else [0, 0, 0]

        # Decide routing
        strategy = {
            'type': 'hybrid',  # Use both semantic + keyword
            'titles_embedding': titles_embedding,
            'goals_embedding': goals_embedding,
            'semantic_weight': 0.6,
            'keyword_weight': 0.4
        }

        self.routing_decisions.append(strategy)

        print(f"\n🧭 {self.name}: Routing analysis complete")
        print(f"   Strategy: {strategy['type']}")
        print(f"   Semantic weight: {strategy['semantic_weight']}")
        print(f"   Keyword weight: {strategy['keyword_weight']}")

        return strategy


# ============================================
# AGENT 2: Semantic Searcher (NEW)
# ============================================

class SemanticJobSearcher:
    """
    SPECIALIZATION: Semantic search for jobs

    Instead of matching keywords, finds jobs similar to:
    - Your goals
    - Your values
    - Your interests
    """

    def __init__(self, name="SemanticSearcher"):
        self.name = name
        self.job_database = [
            {
                "id": 1,
                "title": "Customer Success Manager",
                "company": "Shopify",
                "salary": 65000,
                "location": "Toronto, Canada",
                "description": "Help customers succeed with our platform. Manage relationships, solve problems, provide support."
            },
            {
                "id": 2,
                "title": "Customer Onboarding Specialist",
                "company": "Slack",
                "salary": 52000,
                "location": "Remote",
                "description": "Welcome new customers, implement solutions, ensure smooth onboarding."
            },
            {
                "id": 3,
                "title": "Implementation Consultant",
                "company": "Salesforce",
                "salary": 75000,
                "location": "Remote",
                "description": "Deploy and customize CRM solutions. Technical problem-solving and consulting."
            },
            {
                "id": 4,
                "title": "Project Manager",
                "company": "Asana",
                "salary": 72000,
                "location": "Remote",
                "description": "Lead projects, manage teams, deliver results. Coordinate across departments."
            },
            {
                "id": 5,
                "title": "Solutions Consultant",
                "company": "Stripe",
                "salary": 80000,
                "location": "Remote",
                "description": "Advise clients on technical solutions. Consult on implementation strategy."
            },
            {
                "id": 6,
                "title": "Tech Support Specialist",
                "company": "GitHub",
                "salary": 50000,
                "location": "Remote",
                "description": "Provide technical support. Help developers solve problems with our platform."
            },
        ]

    def search_semantic(self, preferences, routing_strategy):
        """
        Search for jobs using semantic similarity
        """
        print(f"\n🔍 {self.name}: Semantic search starting...")

        goals = preferences.get('goals', '')
        goals_embedding = routing_strategy['goals_embedding']

        scored_jobs = []

        for job in self.job_database:
            # Create embedding for job description + title
            job_text = f"{job['title']} {job['description']}"
            job_embedding = simple_embedding(job_text)

            # Calculate similarity to user's goals
            similarity = cosine_similarity(goals_embedding, job_embedding)

            scored_jobs.append({
                **job,
                'similarity_score': similarity
            })

        # Sort by similarity (highest first)
        scored_jobs.sort(key=lambda x: x['similarity_score'], reverse=True)

        print(f"   ✓ Scored {len(scored_jobs)} jobs by semantic match")

        return scored_jobs


# ============================================
# AGENT 3: Explainer (NEW)
# ============================================

class ExplainerAgent:
    """
    SPECIALIZATION: Explain WHY a job matches

    Instead of just "Applied to X job", explains:
    - Why the match is good
    - What values align
    - What opportunities exist
    """

    def __init__(self, name="Explainer"):
        self.name = name
        self.explanations_generated = 0

    def explain_match(self, job, user_goals, similarity_score):
        """
        Generate explanation why job matches
        """
        self.explanations_generated += 1

        # Simple explanation logic
        if similarity_score > 0.7:
            reason = f"Strong match! This role aligns with your goals around '{user_goals}'."
        elif similarity_score > 0.5:
            reason = f"Good match. This role relates to your interests in '{user_goals}'."
        else:
            reason = f"Interesting opportunity. Consider how '{user_goals}' could apply here."

        explanation = f"""
        Job: {job['title']} at {job['company']}
        Match Score: {similarity_score:.0%}
        Why: {reason}
        """

        return explanation


# ============================================
# NEW ORCHESTRATOR: RAG-Enhanced
# ============================================

class RAGJobOrchestrator:
    """
    Enhanced orchestrator with RAG capabilities

    Workflow:
    1. RAGRouter analyzes preferences
    2. SemanticSearcher finds matching jobs
    3. Explainer explains why they match
    4. Applier applies to top matches
    5. Emailer sends follow-ups
    """

    def __init__(self):
        self.router = RAGRouter()
        self.semantic_searcher = SemanticJobSearcher()
        self.explainer = ExplainerAgent()
        print(f"\n✓ RAG Orchestrator initialized with semantic agents")

    def run(self, preferences):
        """
        Execute RAG-enhanced workflow
        """
        print("\n" + "=" * 60)
        print("RAG-ENHANCED JOB SEARCH WORKFLOW")
        print("=" * 60)

        # STEP 1: Route the search
        routing_strategy = self.router.analyze_preferences(preferences)

        # STEP 2: Semantic search
        scored_jobs = self.semantic_searcher.search_semantic(preferences, routing_strategy)

        # STEP 3: Get top matches
        top_matches = scored_jobs[:5]  # Top 5 matches

        print(f"\n🏆 Top {len(top_matches)} Semantic Matches:")
        explanations = []

        for i, job in enumerate(top_matches, 1):
            # Generate explanation
            explanation = self.explainer.explain_match(
                job,
                preferences.get('goals', ''),
                job['similarity_score']
            )
            explanations.append(explanation)

            print(f"\n{i}. {job['title']} at {job['company']}")
            print(f"   Salary: ${job['salary']}CAD")
            print(f"   Match Score: {job['similarity_score']:.0%}")
            print(f"   Location: {job['location']}")

        return {
            'status': 'success',
            'jobs_found': len(scored_jobs),
            'top_matches': top_matches,
            'explanations': explanations,
            'routing_strategy': routing_strategy
        }


# ============================================
# USAGE: RAG in Action
# ============================================

print("\n" + "🧠" * 30)
print("PHASE 3: SEMANTIC JOB MATCHING")
print("🧠" * 30)

# Create RAG orchestrator
rag_orchestrator = RAGJobOrchestrator()

# Your preferences WITH goals
your_preferences = {
    "titles": ["Customer Success", "Customer Onboarding", "Implementation Consultant"],
    "location": "Canada",
    "salary_min": 50000,
    "goals": "I want to help customers succeed and solve technical problems. I love learning new technologies."
}

# Run RAG workflow
result = rag_orchestrator.run(your_preferences)

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"Total jobs analyzed: {result['jobs_found']}")
print(f"Top semantic matches: {len(result['top_matches'])}")
print(f"Routing strategy: {result['routing_strategy']['type']}")


# ============================================
# CHALLENGE 3: RAG Enhancements
# ============================================

print("\n" + "🚀" * 30)
print("CHALLENGES FOR PHASE 3")
print("🚀" * 30)

print("""
CHALLENGE 1: Add memory to the agent
- Create a MemoryAgent that remembers:
  * Past applications
  * Rejected companies
  * Accepted offers
- Use this memory to improve future searches

CHALLENGE 2: Add company fit analysis
- Analyze job descriptions for:
  * Company size (startup vs enterprise)
  * Tech stack
  * Company culture
- Match against user preferences

CHALLENGE 3: Build a vector database
- Instead of cosine similarity on demo vectors
- Use real embeddings (sentence-transformers library)
- Store jobs in a vector database
- Query by semantic similarity

BONUS: Implement feedback loop
- User rates job matches (1-5)
- Agent learns from feedback
- Improves future recommendations

Hints:
1. MemoryAgent class with save/load methods
2. Parse job descriptions for tech keywords
3. pip install sentence-transformers, faiss-cpu
""")

print("\n✅ Phase 3 Complete!")
print("Next: Move to Phase 4 - Evaluation & Safety")
