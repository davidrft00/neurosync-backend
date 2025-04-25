from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os

# Inicializa o cliente OpenAI com a chave da variável de ambiente
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

# Libera acesso do frontend (pode restringir por domínio se quiser)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # coloca o domínio do teu frontend aqui se for mais seguro
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo do corpo da requisição
class PromptRequest(BaseModel):
    prompt: str

@app.get("/")
async def root():
    return {"message": "NeuroSync AI Backend is running"}

@app.post("/neurosync")
async def neurosync(request: PromptRequest):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": request.prompt}]
        )
        return {"response": response.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}
