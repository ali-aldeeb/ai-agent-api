import asyncio
import logging
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# ---------- OpenRouter Client ----------
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"), 
) 

# ---------- Logging Configuration ----------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# Using name ensures the logger identifies this specific file
logger = logging.getLogger(__name__)

# ---------- Config ----------
MAX_RETRIES = 3
TIMEOUT_SECONDS = 20 # Increased to 20s as free models can be slower
RETRY_DELAY_SECONDS = 2


# ---------- LLM Function ----------
async def ask_llm(prompt: str) -> str:
    

    logger.info("LLM request received")

    last_error = None

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            logger.info(f"LLM attempt {attempt}")

           
            response = await asyncio.wait_for(
                asyncio.to_thread(
                    client.chat.completions.create,
                    model="openai/gpt-oss-20b:free", 
                    messages=[{"role": "user", "content": prompt}]
                ),
                timeout=TIMEOUT_SECONDS
            )

            logger.info("LLM response successful")
            
            return response.choices[0].message.content

        except Exception as e:
            last_error = e
            logger.warning(f"LLM attempt {attempt} failed: {e}")

            if attempt < MAX_RETRIES:
                await asyncio.sleep(RETRY_DELAY_SECONDS)

    logger.error("LLM failed after maximum retries")
    raise RuntimeError(f"LLM failed after {MAX_RETRIES} retries: {last_error}")