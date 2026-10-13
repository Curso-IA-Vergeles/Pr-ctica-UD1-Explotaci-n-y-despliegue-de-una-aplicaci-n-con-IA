import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI, APIError, AuthenticationError

# Cargar variables de entorno desde el nivel superior del proyecto
load_dotenv(dotenv_path="../.env")

app = FastAPI(title="Miniapp IA - Resumidor")

# Inicialización diferida del cliente para evitar fallos fatales en tiempo de importación
api_key = os.getenv("AI_PROVIDER_API_KEY")
base_url = os.getenv("AI_BASE_URL")
ai_model = os.getenv("AI_MODEL", "gemini-3.5-flash")

client = OpenAI(api_key=api_key, base_url=base_url) if api_key else None

class RequestData(BaseModel):
    texto: str

class ResponseData(BaseModel):
    resumen: str

@app.get("/api/health")
def health_check():
    """Endpoint de liveness para validación de despliegue en orquestadores y balanceadores."""
    return {"status": "ok"}

@app.post("/api/generar", response_model=ResponseData)
def generar_resumen(data: RequestData):
    """
    Procesa el texto de entrada delegando la generación a la API de OpenAI.
    Implementa validación de payload y enmascaramiento de errores upstream.
    """
    if not data.texto.strip():
        raise HTTPException(status_code=400, detail="El payload 'texto' es obligatorio y no puede estar vacío.")
    
    if not client:
        raise HTTPException(status_code=500, detail="La configuración del proveedor de IA no está inicializada.")

    try:
        response = client.chat.completions.create(
            model=ai_model,
            messages=[
                {"role": "system", "content": "Eres un asistente técnico experto en extraer resúmenes concisos de una sola frase."},
                {"role": "user", "content": f"Resume este texto: {data.texto}"}
            ],
            max_tokens=150,
            temperature=0.2
        )
        return ResponseData(resumen=response.choices[0].message.content.strip())

    except AuthenticationError:
        raise HTTPException(status_code=401, detail="Fallo de autorización al contactar con el proveedor de IA.")
    except APIError:
        raise HTTPException(status_code=502, detail="Error de comunicación o timeout con el servicio externo.")
    except Exception:
        # En un entorno de producción, la traza real se enviaría al sistema de logs centralizado
        raise HTTPException(status_code=500, detail="Error interno del servidor durante el procesamiento.")