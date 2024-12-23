import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import google.generativeai as genai

# Configure a API do Google Gemini com sua chave
genai.configure(api_key="AIzaSyCuKxOa7GoY6id_aG-C3_uhvfJ1iI0SeQ0")

# Crie a aplicação FastAPI
app = FastAPI()

# Configurações do modelo
generation_config = {
    "temperature": 0.15,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="PROMPT",
)

@app.post("/message")
async def handle_message(request: Request):
    data = await request.json()
    user_message = data.get("user_message")  # Captura a mensagem do usuário enviada pelo Poe
    
    if not user_message:
        return JSONResponse(content={"error": "Mensagem do usuário não encontrada."}, status_code=400)
    
    # Inicia uma sessão de chat
    chat_session = model.start_chat(history=[])
    
    # Envia a mensagem do usuário e obtém a resposta
    response = chat_session.send_message(user_message)
    
    # Retorna a resposta em formato JSON
    return JSONResponse(content={"response": response.text})

# Rodar o servidor FastAPI
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
