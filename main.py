import os
import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from strands import Agent
from strands.models.ollama import OllamaModel
from tools.calculator import calculator

load_dotenv()

OLLAMA_HOST = os.getenv("OLLAMA_BASE_URL")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")
API_HOST = os.getenv("API_HOST")
API_PORT = int(os.getenv("API_PORT"))

app = FastAPI(
    title="AI Chat Agent Dreamsquad",
    description="API de Chat com Agente de IA da Dreamsquad capaz de realizar cálculos matemáticos",
    version="1.0.0"
)

class ChatRequest(BaseModel):
    """Esse é o modelo para requisição de chat"""
    message: str = Field(..., description="Mensagem do usuário", min_length=1)
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Quanto é 1234 * 5678?"
            }
        }


class ChatResponse(BaseModel):
    """Esse é o modelo para resposta de chat"""
    response: str = Field(..., description="Resposta do agente de IA")
    
    class Config:
        json_schema_extra = {
            "example": {
                "response": "O resultado de 1234 * 5678 é 7006652."
            }
        }


def get_event_loop():
    try:
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        return loop
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop


def create_agent():
    model = OllamaModel(
        host=OLLAMA_HOST,
        model_id=OLLAMA_MODEL,
        temperature=0.7
    )
    
    system_prompt = """Você é um assistente útil e amigável que pode responder perguntas de conhecimento geral em português.

    Você tem acesso a uma ferramenta de calculadora, mas deve usá-la APENAS quando o usuário fizer uma pergunta que claramente requer um cálculo matemático.

    QUANDO USAR A FERRAMENTA CALCULATOR:
    - Perguntas explícitas de cálculo: "Quanto é 1234 * 5678?"
    - Operações matemáticas: "Calcule 2 elevado a 10"
    - Raízes e funções: "Qual a raiz quadrada de 144?"
    - Expressões numéricas: "Quanto é (15 + 25) / 2?"

    QUANDO NÃO USAR A FERRAMENTA (responda diretamente):
    - Cumprimentos: "Olá!", "Oi!", "Tudo bem?"
    - Perguntas gerais: "O que é inteligência artificial?"
    - Conversas casuais: "Como você está?", "Qual seu nome?"
    - Conhecimento geral: "Quem foi Einstein?", "O que é FastAPI?"

    Para perguntas que requerem cálculos básicos, cálculos complexos ou que exigem precisão, use a ferramenta calculator.
    Para todo o resto, responda diretamente de forma amigável e informativa."""
    
    agent = Agent(
        model=model,
        tools=[calculator],
        system_prompt=system_prompt,
        state=None 
    )
    
    return agent


@app.on_event("startup")
async def startup_event():
    try:
        test_agent = create_agent()
        print(f"✅ Agente inicializado com sucesso!")
        print(f"📦 Modelo: {OLLAMA_MODEL}")
        print(f"🌐 Host Ollama: {OLLAMA_HOST}")
        print(f"🔧 Tools disponíveis: {test_agent.tool_names}")
    except Exception as e:
        print(f"❌ Erro ao inicializar o agente: {e}")
        print(f"⚠️  Verifique se o Ollama está rodando: ollama serve")


@app.get("/")
async def root():
    """Esse é o endpoint raiz com informações da API"""
    return {
        "message": "Chat Agent API está funcionando! ✅",
        "endpoints": {
            "chat": "/chat",
            "health": "/health",
            "docs": "/docs"
        },
        "model": OLLAMA_MODEL,
        "ollama_host": OLLAMA_HOST,
        "note": "Cada requisição é independente (sem memória entre chamadas)"
    }


@app.get("/health")
async def health_check():
    try:
        test_agent = create_agent()
        return {
            "status": "healthy",
            "model": OLLAMA_MODEL,
            "ollama_host": OLLAMA_HOST,
            "tools_loaded": len(test_agent.tool_names),
            "tools": test_agent.tool_names
        }
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Serviço indisponível: {str(e)}"
        )


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Endpoint para processar a mensagem dos usuários
    """
    try:
        loop = get_event_loop()
        
        agent = create_agent()
        
        def run_agent():
            response = agent(request.message)
            return response
        
        response = await loop.run_in_executor(None, run_agent)
        
        if isinstance(response, str):
            agent_response = response
        elif hasattr(response, 'content'):

            if isinstance(response.content, list):

                text_parts = [
                    item.get('text', '') 
                    for item in response.content 
                    if isinstance(item, dict) and 'text' in item
                ]
                agent_response = '\n'.join(text_parts) if text_parts else str(response.content)
            else:
                agent_response = response.content
        else:
            agent_response = str(response)
        
        return ChatResponse(response=agent_response.strip())
    
    except Exception as e:

        print(f"❌ Erro ao processar mensagem '{request.message}': {str(e)}")
        import traceback
        traceback.print_exc()
        
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao processar a mensagem: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*50)
    print("🚀 Iniciando Chat Agent API")
    print("="*50)
    print(f"📍 URL: http://{API_HOST}:{API_PORT}")
    print(f"📚 Documentação: http://{API_HOST}:{API_PORT}/docs")
    print(f"🤖 Modelo: {OLLAMA_MODEL}")
    print(f"🌐 Ollama Host: {OLLAMA_HOST}")
    print(f"💡 Cada requisição é independente")
    print("="*50 + "\n")
    
    uvicorn.run(
        "main:app",
        host=API_HOST,
        port=API_PORT,
        reload=True
    )