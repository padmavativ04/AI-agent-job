"""
Phase 5: Voice Agents & Voice Interface
========================================

Learn to build voice-enabled AI agents that can:
1. Listen to user speech (STT - Speech-to-Text)
2. Process with AI
3. Respond with speech (TTS - Text-to-Speech)

Key Concepts:
- Speech Recognition (Web Audio API)
- Natural Language Understanding
- Voice Synthesis
- Real-time Processing
- Conversational AI
"""

from complete_agent import Orchestrator
from datetime import datetime
import json


# ============================================
# LESSON 1: Understanding Voice Agents
# ============================================

"""
Voice Agent Flow:

User speaks: "Find me customer success jobs in Canada"
    ↓
STT (Speech-to-Text): Converts audio → text
    ↓
NLP (Natural Language Processing): Understands intent
    ↓
Agent Processing: Searches jobs, applies, generates response
    ↓
TTS (Text-to-Speech): Converts response → audio
    ↓
Speaker plays: "Found 5 customer success jobs in Canada..."

Why Voice Agents?
✅ Hands-free operation
✅ Natural interaction
✅ Accessibility
✅ Faster than typing
✅ More engaging
"""


# ============================================
# LESSON 2: Voice Agent Class
# ============================================

class VoiceAgent:
    """
    A voice-enabled job application agent

    Capabilities:
    - Listen to user voice commands
    - Understand intent
    - Process with AI agent
    - Respond with voice
    """

    def __init__(self, name="VoiceJobAgent"):
        self.name = name
        self.orchestrator = Orchestrator()
        self.conversation_history = []
        self.is_listening = False

        print(f"✓ {self.name} initialized")
        print("🎤 Ready to listen!")

    def process_voice_input(self, text_input: str) -> dict:
        """
        Process voice input and return voice response

        Input: "Find me customer success jobs in Canada"
        Output: Dictionary with response text and audio
        """
        print(f"\n👂 You said: {text_input}")

        # Step 1: Extract intent from text
        intent = self._extract_intent(text_input)
        print(f"🧠 Intent detected: {intent['action']}")

        # Step 2: Convert intent to preferences
        preferences = self._intent_to_preferences(intent)
        print(f"🔍 Searching with preferences: {preferences}")

        # Step 3: Run agent
        result = self.orchestrator.run(preferences)

        # Step 4: Generate voice response
        response_text = self._generate_response(intent, result)

        # Step 5: Log conversation
        self._log_conversation(text_input, response_text)

        return {
            "status": "success",
            "user_input": text_input,
            "intent": intent,
            "response_text": response_text,
            "search_results": result
        }

    def _extract_intent(self, text: str) -> dict:
        """
        Extract user intent from text

        Examples:
        - "Find customer success jobs" → action: 'search'
        - "Apply to jobs" → action: 'apply'
        - "Show my applications" → action: 'show_applications'
        """
        text_lower = text.lower()

        # Intent detection logic (simplified)
        if any(word in text_lower for word in ['find', 'search', 'look for']):
            action = 'search'
        elif any(word in text_lower for word in ['apply', 'apply to']):
            action = 'apply'
        elif any(word in text_lower for word in ['show', 'list', 'what are']):
            action = 'show'
        else:
            action = 'unknown'

        # Extract job titles
        job_titles = self._extract_job_titles(text)

        # Extract location
        location = self._extract_location(text)

        return {
            "action": action,
            "job_titles": job_titles,
            "location": location,
            "confidence": 0.85
        }

    def _extract_job_titles(self, text: str) -> list:
        """Extract job titles from text"""
        keywords = {
            'customer success': ['customer success', 'success manager'],
            'implementation': ['implementation', 'consultant'],
            'project manager': ['project manager', 'pm'],
            'solutions': ['solutions', 'consultant'],
            'support': ['support', 'tech support'],
        }

        found_titles = []
        for title, keywords_list in keywords.items():
            for keyword in keywords_list:
                if keyword.lower() in text.lower():
                    found_titles.append(title)
                    break

        return found_titles if found_titles else ['Customer Success', 'Implementation Consultant']

    def _extract_location(self, text: str) -> str:
        """Extract location from text"""
        locations = ['canada', 'remote', 'toronto', 'vancouver', 'calgary']
        for location in locations:
            if location.lower() in text.lower():
                return location.capitalize()
        return 'Canada'

    def _intent_to_preferences(self, intent: dict) -> dict:
        """Convert intent to agent preferences"""
        return {
            "titles": intent.get("job_titles", ["Customer Success"]),
            "location": intent.get("location", "Canada"),
            "salary_min": 50000,
            "goals": f"Looking for {', '.join(intent.get('job_titles', ['jobs']))} roles"
        }

    def _generate_response(self, intent: dict, result: dict) -> str:
        """
        Generate natural language response

        This will be converted to speech (TTS)
        """
        action = intent['action']

        if action == 'search':
            jobs_found = result.get('jobs', [])
            apps_made = result.get('applications', [])

            if not jobs_found:
                return "I didn't find any matching jobs. Try different keywords."

            response = f"Great! I found {len(jobs_found)} matching jobs. "
            response += f"Applied to {len(apps_made)} jobs. "
            response += f"Top match: {jobs_found[0]['title']} at {jobs_found[0]['company']}. "
            response += "Would you like details on any of these?"

            return response

        elif action == 'show':
            apps = result.get('applications', [])
            return f"You have {len(apps)} applications. Total jobs found: {len(result.get('jobs', []))}."

        else:
            return "I didn't understand that. You can say 'find jobs', 'apply to jobs', or 'show my applications'."

    def _log_conversation(self, user_input: str, response: str):
        """Log conversation for history"""
        self.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "user": user_input,
            "agent": response
        })

    def get_conversation_history(self) -> list:
        """Get full conversation history"""
        return self.conversation_history

    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []


# ============================================
# LESSON 3: Conversational Context
# ============================================

class ConversationalVoiceAgent(VoiceAgent):
    """
    Extended voice agent with context awareness

    Remembers previous messages to maintain conversation context
    """

    def __init__(self, name="ConversationalVoiceAgent"):
        super().__init__(name)
        self.context = {}
        self.last_search_results = None

    def process_with_context(self, text_input: str) -> dict:
        """Process input considering conversation context"""

        # Check if follow-up to previous search
        if self._is_follow_up(text_input):
            # Use cached results
            return self._handle_follow_up(text_input)
        else:
            # New search
            result = self.process_voice_input(text_input)
            self.last_search_results = result
            return result

    def _is_follow_up(self, text: str) -> bool:
        """Check if this is a follow-up to previous message"""
        follow_up_keywords = [
            'that one', 'the first', 'the second',
            'more details', 'tell me more',
            'yes', 'no', 'okay', 'sure'
        ]

        return any(keyword in text.lower() for keyword in follow_up_keywords)

    def _handle_follow_up(self, text: str) -> dict:
        """Handle follow-up questions"""
        if not self.last_search_results:
            return {"error": "No previous search to follow up on"}

        response_text = f"Based on your previous search, {text.lower()}. "
        response_text += "Here are the details..."

        return {
            "status": "success",
            "type": "follow_up",
            "user_input": text,
            "response_text": response_text,
            "previous_results": self.last_search_results
        }


# ============================================
# LESSON 4: Voice Commands
# ============================================

VOICE_COMMANDS = {
    "search": [
        "find {job} jobs in {location}",
        "search for {job}",
        "look for {job} in {location}",
        "show me {job} positions"
    ],
    "apply": [
        "apply to all matching jobs",
        "apply to the first job",
        "submit applications"
    ],
    "show": [
        "show my applications",
        "list my applications",
        "how many jobs have i applied to",
        "show results"
    ],
    "help": [
        "help",
        "what can you do",
        "tell me what you can do",
        "guide me"
    ]
}


def print_voice_commands():
    """Print available voice commands"""
    print("\n📋 Available Voice Commands:\n")
    for action, commands in VOICE_COMMANDS.items():
        print(f"📢 {action.upper()}:")
        for cmd in commands:
            print(f"   • \"{cmd}\"")
        print()


# ============================================
# EXAMPLE USAGE
# ============================================

if __name__ == "__main__":
    print("=" * 60)
    print("PHASE 5: VOICE AGENTS & VOICE INTERFACE")
    print("=" * 60)

    # Create voice agent
    agent = VoiceAgent()

    # Show available commands
    print_voice_commands()

    # Example voice interactions
    print("\n" + "=" * 60)
    print("EXAMPLE INTERACTIONS")
    print("=" * 60)

    voice_inputs = [
        "Find me customer success and implementation consultant jobs in Canada",
        "Show my applications",
        "Tell me about the first job"
    ]

    for user_input in voice_inputs:
        print(f"\n{'🎤 User:':15} {user_input}")

        result = agent.process_voice_input(user_input)

        print(f"{'🤖 Agent:':15} {result['response_text']}")

    # Show conversation history
    print("\n" + "=" * 60)
    print("CONVERSATION HISTORY")
    print("=" * 60)
    print(json.dumps(agent.get_conversation_history(), indent=2))

    print("\n✅ Phase 5 Complete!")
    print("\nNext: Integrate with Web Audio API for real voice I/O")
