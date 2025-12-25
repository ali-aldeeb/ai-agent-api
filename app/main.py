from fastapi import FastAPI, HTTPException
from schemas import PromptRequest, PromptResponse
from llm import ask_llm
import logging

# ---------- Logging Configuration ----------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)

# ---------- FastAPI App Initialization ----------
app = FastAPI(
    title="AI Agent API",
    description="A robust API to interact with OpenRouter LLMs",
    version="1.0.0"
)

# ---------- API Endpoints ----------

@app.get("/")
async def root():
    """Health check endpoint to ensure the API is running."""
    return {"status": "online", "message": "AI Agent API is ready"}

@app.post("/ask", response_model=PromptResponse)
async def ask_ai(request: PromptRequest):
    """
    Main endpoint to receive prompts and return AI-generated responses.
    This endpoint demonstrates the flow of data through Schemas and the LLM logic.
    """
    logger.info(f"Received request: {request.prompt[:50]}...") # Log the first 50 chars

    try:
        # Step 1: Send the prompt to our LLM function (which handles retries and OpenRouter)
        ai_answer = await ask_llm(request.prompt)
        
        # Step 2: Return the answer using the PromptResponse Schema
        # FastAPI will automatically convert this to JSON for the client
        return PromptResponse(response=ai_answer)

    except RuntimeError as e:
        # Step 3: Catch the escalated error from llm.py and return a clear HTTP error
        logger.error(f"Error in ask_ai: {str(e)}")
        raise HTTPException(
            status_code=502, 
            detail=f"The AI service is currently unavailable. Error: {str(e)}"
        )
    except Exception as e:
        # Catch any other unexpected errors
        logger.critical(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail="An unexpected internal server error occurred."
        )

# To run this app:
# uvicorn app.main:app --reload