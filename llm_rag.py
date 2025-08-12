from langchain.llms import Ollama
from langchain.prompts import PromptTemplate
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

llm = Ollama(model="llama3")

def get_tone_score(text: str) -> str:
    prompt = PromptTemplate.from_template(
        "Analyze the tone of the following email and return one word (e.g., Professional, Friendly, Casual, Rude):\n\n{text}"
    )
    final_prompt = prompt.format(text=text)
    logger.info("Prompting LLM for tone score...")
    return llm(final_prompt)

def rewrite_to_professional(text: str) -> str:
    prompt = PromptTemplate.from_template(
        "Rewrite the following email to sound more professional while keeping the meaning the same:\n\n{text}"
    )
    final_prompt = prompt.format(text=text)
    logger.info("Prompting LLM for professional rewrite...")
    return llm(final_prompt)
