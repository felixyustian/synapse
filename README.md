# Synapse — AI-Powered Meeting Assistant

**Turn Conversations into Actions. Instantly.**

Synapse is a full-stack, deployment-ready AI meeting assistant. Paste any meeting transcript and receive an executive summary, action items with owners and deadlines, key decisions, and a complete follow-up email draft — all powered by Claude.

---

## ✨ Features

| Feature | Description |
|---|---|
| 📋 **Executive Summary** | Concise 3–5 sentence overview of the meeting |
| ✅ **Action Item Extraction** | Tasks with assigned owner, deadline, and priority |
| ⚖️ **Decision Logging** | All key decisions with rationale and impact |
| ✉️ **Follow-Up Email Draft** | Ready-to-send email — just review and hit send |
| 🏷️ **Key Topic Detection** | High-level themes from the conversation |

---

## 🏗️ Architecture

```
synapse/
├── backend/          # FastAPI Python backend
│   ├── main.py       # API routes & Claude integration
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/         # Static HTML/JS/CSS UI
│   ├── index.html    # Single-page application
│   ├── nginx.conf    # Nginx reverse proxy config
│   └── Dockerfile
├── .github/
│   └── workflows/
│       └── ci.yml    # GitHub Actions CI pipeline
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose installed
- An [Anthropic API key](https://console.anthropic.com/)

### 1. Clone the repository
```bash
git clone https://github.com/felixyustian/synapse.git
cd synapse
```

### 2. Set up environment variables
```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### 3. Launch with Docker Compose
```bash
docker compose up --build
```

**That's it.** Open [http://localhost](http://localhost) in your browser.

---

## 🛠️ Local Development (without Docker)

### Backend
```bash
cd backend
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your_key_here
uvicorn main:app --reload --port 8000
```
API docs available at: [http://localhost:8000/docs](http://localhost:8000/docs)

### Frontend
```bash
# The frontend is plain HTML — just open it in a browser:
open frontend/index.html

# Or serve it with any static server:
cd frontend && python -m http.server 3000
```

---

## 🔌 API Reference

### `POST /api/analyze`

Analyzes a meeting transcript and returns structured insights.

**Request Body:**
```json
{
  "transcript": "Alice: We need to finalize the budget...",
  "meeting_title": "Q3 Planning Sync",
  "attendees": ["Alice", "Bob", "Carol"]
}
```

**Response:**
```json
{
  "summary": "The team aligned on a product launch for the 30th...",
  "key_topics": ["Launch Timeline", "Budget", "Staging Environment"],
  "action_items": [
    {
      "task": "Set up QA staging environment",
      "owner": "Bob",
      "deadline": "End of day tomorrow",
      "priority": "High"
    }
  ],
  "decisions": [
    {
      "decision": "David reassigned to load testing",
      "rationale": "Load testing is on the critical path for the launch",
      "impact": "Admin panel work delayed"
    }
  ],
  "follow_up_email": "Subject: Meeting Notes — Q3 Planning Sync\n\nHi team..."
}
```

### `GET /health`
Health check endpoint — returns `{"status": "healthy"}`.

---

## ☁️ Cloud Deployment

### Render
1. Push to GitHub
2. Create two Render services — a **Web Service** (backend) and a **Static Site** (frontend)
3. Set `ANTHROPIC_API_KEY` as an environment variable in the backend service

### Railway / Fly.io
Use the provided `docker-compose.yml` as the base configuration. Both platforms support Docker Compose deployments natively.

### VPS (DigitalOcean, AWS EC2, etc.)
```bash
# On the server:
git clone https://github.com/felixyustian/synapse.git
cd synapse
cp .env.example .env && nano .env  # Add your API key
docker compose up -d
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m 'feat: add my feature'`
4. Push to the branch: `git push origin feature/my-feature`
5. Open a Pull Request

---

## 📄 License

GPL-3.0 License — see [LICENSE](LICENSE) for details.
