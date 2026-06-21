from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from search import search_engine

app = FastAPI(
    title="NayePankh AI Assistant"
)

# Enable CORS so React can talk to FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Later restrict this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def root():
    return {
        "message": "NayePankh AI Assistant Backend Running"
    }

@app.post("/chat")
def chat(request: ChatRequest):

    result = search_engine.search(request.message)

    return {
        "answer": result["answer"],
        "confidence": result["confidence"],
        "matched_question": result["matched_question"]
    }