# AI Job Application Agent

An intelligent multi-agent system for automated job applications with voice interface.

## Features
- 🤖 Multi-agent architecture (Searcher, Applier, Emailer)
- 🔍 Semantic job matching with RAG
- 🎤 Voice interface (speech-to-text, text-to-speech)
- 💾 Persistent memory of applications
- ⚡ Real-time feedback collection

## Tech Stack
- **Backend:** Python (Flask), PostgreSQL
- **Frontend:** React, JavaScript
- **Voice:** Web Audio API
- **AI:** OpenAI/Claude APIs

## Project Structure
```
AI-agent-job/
├── backend/
│   ├── agents/          # Agent definitions
│   ├── skills/          # Reusable agent skills
│   ├── app.py           # Flask server
│   └── requirements.txt
├── frontend/
│   ├── src/             # React components
│   ├── public/
│   └── package.json
├── docs/                # Documentation
└── README.md
```

## Timeline
- **Week 1:** Python fundamentals + Job Searcher agent
- **Week 2:** Multi-agent architecture (Searcher, Applier, Emailer)
- **Week 3:** RAG & vector search for semantic matching
- **Week 4:** Evaluation metrics & safety guardrails
- **Week 5:** React frontend + Web Audio API voice
- **Week 6:** Deployment & polish

## Getting Started
```bash
# Clone the repo
git clone https://github.com/padmavativ04-create/AI-agent-job.git
cd AI-agent-job

# Install backend dependencies
cd backend
pip install -r requirements.txt

# Install frontend dependencies
cd ../frontend
npm install

# Start coding!
```

## Author
[Your Name]

## License
MIT
