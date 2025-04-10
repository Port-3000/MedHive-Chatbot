
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def root():
    return{
        "messaage": "Chatbot API",
        "version": "1.0.0",
    }