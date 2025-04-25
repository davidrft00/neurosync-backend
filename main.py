from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os

openai.api_key = os.getenv("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")

app = FastAPI()

# Libera acesso do frontend (se for usar)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    prompt: str

@app.get("/")
async def root():
    return {"message": "NeuroSync AI Backend is running"}

@app.post("/neurosync")
async def neurosync(request: PromptRequest):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": request.prompt}]
        )
        return {"response": response['choices'][0]['message']['content']}
    except Exception as e:
        return {"error": str(e)}

