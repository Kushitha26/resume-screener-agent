import os
import json
from dotenv import load_dotenv
from groq import Groq

"""
Tools & Technologies (as per challenge):

AI Models: (e.g.) OpenAI GPT, Claude, Gemini
Frameworks: (can be extended with) LangChain, CrewAI, LlamaIndex
Vector DBs: Pinecone, ChromaDB, Weaviate, FAISS
UI: Streamlit (used in this project), Gradio, HTML/JS
APIs: Google Calendar, Zapier, Notion, Sheets, Calendly, Shopify
Databases: Firebase, Supabase, Notion DB, Google Sheets

In this implementation:
- We actively use: an AI model via Groq (Llama 3) + Streamlit for UI.
- The rest are options that can be integrated later (mentioned in README).
"""

# Load .env
load_dotenv()

# Create Groq client (using free Llama models)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def screen_resume(jd_text: str, resume_text: str) -> dict:
    """
    Compare a candidate's resume to the Job Description using Groq (Llama 3.1 8B).
    Returns a structured JSON-style result with match score, fit level, etc.
    """

    prompt = f"""
You are an ATS-style resume screening assistant.

You will receive:
1. Job Description (JD)
2. Candidate Resume

Compare the resume against the JD and respond ONLY in valid JSON with this exact schema:
{{
  "match_score": <integer 0-100>,
  "fit_level": "<one of: Strong, Medium, Weak>",
  "strengths": ["point 1", "point 2", "point 3"],
  "gaps": ["point 1", "point 2"],
  "recommendation": "<one of: Interview, Hold, Reject>",
  "reason_summary": "<2-3 sentences explaining the decision>"
}}

Rules:
- Focus on skills, tech stack, years of experience, domain fit, and education relevance.
- If the resume is very unrelated, keep score below 40 and recommend "Reject".
- Return ONLY JSON. No extra text.

JOB DESCRIPTION:
\"\"\"{jd_text}\"\"\"

RESUME:
\"\"\"{resume_text}\"\"\"
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # current supported Llama model on Groq
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )

        content = response.choices[0].message.content

        # Try to parse JSON from model output
        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            data = {
                "match_score": 0,
                "fit_level": "Weak",
                "strengths": [],
                "gaps": ["Could not parse model output correctly."],
                "recommendation": "Hold",
                "reason_summary": content[:300],
            }

        return data

    except Exception as e:
        # Fallback if API fails – so app still runs
        return {
            "match_score": 0,
            "fit_level": "Weak",
            "strengths": [],
            "gaps": [f"Error: {str(e)}"],
            "recommendation": "Hold",
            "reason_summary": "Error during API call.",
        }
