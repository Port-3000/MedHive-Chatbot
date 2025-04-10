

import os 

CACHE_DIR = "/temp/.cache"
os.environ["TRANSFORMERS_CACHE"] = CACHE_DIR
os.environ["HF_HOME"] = CACHE_DIR

if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR, exist_ok=True)
    
    
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import root, health, chat
from app.services.rag_service import rag_service


app = FastAPI()


# Include routes
app.include_router(root.router)
app.include_router(health.router)
app.include_router(chat.router)

@app.on_event("startup")
async def startup_event():
    try:
        # Initialize the RAG system
        rag_service.initialize()
        print("✅ RAG system initialized successfully")
    except Exception as e:
        print(f"❌ RAG initialization failed: {str(e)}")
        raise e
    
