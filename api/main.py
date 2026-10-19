import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai

# Carga de variables compatible con ejecucion desde subdirectorio o raiz en Vercel
load_dotenv(dotenv_path="../.env")
load_dotenv()

app = FastAPI(title="Miniapp IA - Resumidor")

# Inicializacion del cliente oficial de Google GenAI leyendo del entorno del sistema
api_key = os.getenv("AI_PROVIDER_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None

class RequestData(BaseModel):
    texto: str

class ResponseData(BaseModel):
    resumen: str

@app.get("/api/health")
def health_check():
    """
    Verificacion de disponibilidad del servicio serverless.
    """
    return {"status": "ok"}

@app.post("/api/generar", response_model=ResponseData)
def generar_resumen(data: RequestData):
    """
    Controlador principal de generacion de resumenes mediante Gemini 2.5 Flash.
    """
    if not data.texto.strip():
        raise HTTPException(status_code=400, detail="El payload 'texto' es obligatorio.")
    
    if not client:
        raise HTTPException(status_code=500, detail="Configuracion de Google Gemini ausente en el servidor.")

    try:
        prompt = f"Eres un asistente experto en generar resúmenes concisos de una línea. Resume este texto: {data.texto}"
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        
        if not response.text:
            raise ValueError("El modelo devolvio una respuesta vacia.")
            
        return ResponseData(resumen=response.text.strip())
        
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error con Gemini: {str(e)}")