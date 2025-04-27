from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.agent import ask_ai

router = APIRouter()

class QuestionRequest(BaseModel):
    question: str

@router.post("/ask")
async def ask_question(payload: QuestionRequest):
    try:
        print(f"Received question: {payload.question}")
        response = ask_ai(payload.question)
        print(f"Response: {response}")
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
