
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.rag_service import rag_service

router = APIRouter()

class QueryRequest(BaseModel):
    question: str
    coversation_id: str = "default"
    
@router.post("/chat")
async def chat_endpoint(request: QueryRequest):
    try:
        context = rag_service.get_context(request.question)
        response = rag_service.generate_response(request.question, context)
        return{
            "response": response,
            "context": context,
            "conversation_id": request.coversation_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))