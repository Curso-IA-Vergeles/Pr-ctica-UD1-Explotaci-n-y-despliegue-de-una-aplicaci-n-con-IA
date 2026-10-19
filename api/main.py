import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai

# Carga de variables de entorno desde el directorio raiz del proyecto
load_dotenv(dotenv_path="../.env")

app = FastAPI(title="Miniapp IA - Resumidor")

# Inicializacion del cliente oficial de Google GenAI
api_key = os.getenv("AI_PROVIDER_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None

class RequestData(BaseModel):
    texto: str

class ResponseData(BaseModel):
    resumen: str

@app.post("/api/generar", response_model=ResponseData)
def generar_resumen(data: RequestData):
    """
    Recibe un texto desde el frontend y retorna un resumen generado por Gemini.
    """
    if not data.texto.strip():
        raise HTTPException(status_code=400, detail="El payload 'texto' es obligatorio.")
    
    if not client:
        raise HTTPException(status_code=500, detail="Configuracion de Google Gemini ausente en el servidor.")

    try:
        prompt = f"Eres un asistente experto en generar resúmenes concisos de una línea. Resume este texto: {data.texto}"
        
        # Ejecucion de la consulta contra el modelo estandar actual
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        
        if not response.text:
            raise ValueError("El modelo devolvio una respuesta vacia.")
            
        return ResponseData(resumen=response.text.strip())
        
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error con Gemini: {str(e)}")