from fastapi import FastAPI
from typing import List
from models import EmailData, EmailText
from vector_store import add_emails_to_vectorstore, retrieve_similar_emails
from llm_rag import get_tone_score, rewrite_to_professional

app = FastAPI()

@app.post("/ingest_emails")
def ingest_emails(emails: List[EmailData]):
    add_emails_to_vectorstore(emails)
    return {"message": f"{len(emails)} email(s) ingested successfully."}

@app.post("/suggest_recipients")
def suggest_recipients(from_: str, subject: str, body: str, suggest_for: str):
    similar_docs = retrieve_similar_emails(subject=subject, body=body, from_=from_)
    recipients = set()
    for doc in similar_docs:
        metadata = doc.metadata
        if suggest_for == "to":
            recipients.update(str(metadata.get("to", "")).split(","))
        elif suggest_for == "cc":
            recipients.update(str(metadata.get("cc", "")).split(","))
    return {"suggestions": [r.strip() for r in recipients if r.strip()]}

@app.post("/analyze_tone")
def analyze_tone(email: EmailText):
    tone = get_tone_score(email.body).strip()
    professional = rewrite_to_professional(email.body).strip()
    return {
        "detected_tone": tone,
        "professional_version": professional
    }
