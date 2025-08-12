import re
from models import EmailData
from typing import List

# Simple regex-based thread splitter
def extract_thread_emails(body: str, subject: str, from_: str) -> List[EmailData]:
    # Split on common reply separators
    chunks = re.split(r'\n\s*-{2,}|On .+?wrote:|From:.+?\n', body, flags=re.IGNORECASE)
    messages = []

    for chunk in chunks:
        text = chunk.strip()
        if text:
            messages.append(EmailData(
                from_=from_,
                to=[],
                cc=[],
                subject=subject,
                body=text
            ))

    return messages
