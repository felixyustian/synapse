"""
Synapse - AI-Powered Meeting Assistant
FastAPI Backend
"""

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from anthropic import Anthropic
import json

app = FastAPI(
    title="Synapse API",
    description="AI-Powered Meeting Assistant Backend",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# ─── Models ───────────────────────────────────────────────────────────────────

class TranscriptRequest(BaseModel):
    transcript: str
    meeting_title: str = "Team Meeting"
    attendees: list[str] = []

class AnalysisResponse(BaseModel):
    summary: str
    action_items: list[dict]
    decisions: list[dict]
    follow_up_email: str
    key_topics: list[str]

# ─── System Prompt ─────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are Synapse, an expert AI meeting analyst. Your job is to process meeting transcripts and extract structured, actionable information.

Always respond with ONLY valid JSON in exactly this structure (no markdown, no preamble):
{
  "summary": "A concise 3-5 sentence executive summary of the meeting",
  "key_topics": ["topic1", "topic2", ...],
  "action_items": [
    {
      "task": "Specific action to be taken",
      "owner": "Person responsible (or 'Unassigned')",
      "deadline": "Mentioned deadline or 'No deadline specified'",
      "priority": "High | Medium | Low"
    }
  ],
  "decisions": [
    {
      "decision": "What was decided",
      "rationale": "Why this decision was made (if mentioned)",
      "impact": "Who or what this affects"
    }
  ],
  "follow_up_email": "A complete, professional follow-up email ready to send, starting with Subject: ..."
}

Be precise, professional, and thorough. Extract ALL action items and decisions you can identify."""

# ─── Routes ────────────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {"status": "Synapse API is running", "version": "1.0.0"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/api/analyze", response_model=AnalysisResponse)
def analyze_transcript(request: TranscriptRequest):
    if not request.transcript.strip():
        raise HTTPException(status_code=400, detail="Transcript cannot be empty.")

    attendees_str = ", ".join(request.attendees) if request.attendees else "Not specified"

    user_message = f"""Meeting Title: {request.meeting_title}
Attendees: {attendees_str}

TRANSCRIPT:
{request.transcript}

Please analyze this transcript and return the structured JSON."""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=2000,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_message}]
        )

        raw = response.content[0].text.strip()
        # Strip markdown fences if present
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        data = json.loads(raw)

        return AnalysisResponse(**data)

    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="AI response could not be parsed. Try again.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
