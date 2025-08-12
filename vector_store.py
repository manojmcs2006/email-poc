import logging
from typing import List, Optional
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document
from models import EmailData
from thread_parser import extract_thread_emails

# Dummy thread parser
def extract_thread_emails(body: str, subject: str, from_: str) -> List[EmailData]:
    return [EmailData(from_=from_, to=[], cc=[], subject=subject, body=body)]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
CHROMA_PATH = "chroma_db"
db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_model)

def _email_to_doc(email: EmailData) -> Optional[Document]:
    content = f"From: {email.from_}\nSubject: {email.subject}\nBody: {email.body}".strip()
    if not content:
        logger.warning("Skipping empty email.")
        return None

    metadata = {
        "to": ", ".join(email.to) if isinstance(email.to, list) else email.to,
        "cc": ", ".join(email.cc) if isinstance(email.cc, list) else email.cc,
        "from": email.from_,
        "subject": email.subject
    }

    return Document(page_content=content, metadata=metadata)

def add_emails_to_vectorstore(emails: List[EmailData]):
    all_docs = []
    logger.info(f"Ingesting {len(emails)} email(s)...")
    for email in emails:
        thread_emails = extract_thread_emails(email.body, email.subject, email.from_)
        docs = [_email_to_doc(e) for e in thread_emails]
        docs = [doc for doc in docs if doc]
        all_docs.extend(docs)
    if all_docs:
        db.add_documents(all_docs)
        db.persist()
        logger.info(f"Stored {len(all_docs)} documents.")
    else:
        logger.warning("No documents to embed.")

def retrieve_similar_emails(subject: str, body: str, from_: Optional[str], k: int = 5) -> List[Document]:
    query = f"From: {from_}\nSubject: {subject}\nBody: {body}" if from_ else f"Subject: {subject}\nBody: {body}"
    logger.info("Running similarity search...")
    return db.similarity_search(query, k=k)
