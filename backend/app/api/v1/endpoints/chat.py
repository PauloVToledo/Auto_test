from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services import ai_service

router = APIRouter()


class ChatRequest(BaseModel):
    message: str


@router.post("/")
def chat_with_ai(request: ChatRequest, db: Session = Depends(get_db)):
    response = ai_service.get_chat_response(request.message, db)
    return {"response": response}
