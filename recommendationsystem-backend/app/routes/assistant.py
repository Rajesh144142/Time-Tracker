from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.agent import ask_ai
import logging

router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QuestionRequest(BaseModel):
    question: str

@router.post("/ask")
async def ask_question(payload: QuestionRequest):
    """
    Endpoint to handle recommendation questions with verification
    
    Args:
        payload: QuestionRequest containing the user's question
        
    Returns:
        dict: {"response": "answer"} or error message
        
    Raises:
        HTTPException: 500 for server errors, 400 for invalid requests
    """
    try:
        logger.info(f"Received question: {payload.question}")
        
        # Validate question is not empty
        if not payload.question.strip():
            logger.warning("Empty question received")
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        
        # Process the question
        response = ask_ai(payload.question)
        logger.info(f"Generated response: {response}")
        
        return {"response": response}
        
    except TimeoutError as te:
        logger.error(f"Processing timeout: {str(te)}")
        raise HTTPException(status_code=408, detail="Request timed out")
        
    except ValueError as ve:
        logger.error(f"Validation error: {str(ve)}")
        raise HTTPException(status_code=400, detail=str(ve))
        
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing your question"
        )