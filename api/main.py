import os
import jwt
import google.generativeai as genai
from jwt import PyJWKClient
from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from dotenv import load_dotenv

# Carga en memoria de los secretos antes de inicializar los clientes
load_dotenv(dotenv_path="../.env")

app = FastAPI(title="Miniapp IA - Resumidor Protegido")

# Configuracion del cliente de IA de Google Generative AI
api_key = os.getenv("AI_PROVIDER_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    genai = None

# Instanciacion del resolutor JWKS para verificar las firmas RSA de Clerk
jwks_url = os.getenv("CLERK_JWKS_URL")
jwks_client = PyJWKClient(jwks_url) if jwks_url else None
security = HTTPBearer()

class RequestData(BaseModel):
    texto: str

class ResponseData(BaseModel):
    resumen: str

def validar_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    Middleware interceptor para validacion JWT.
    Extrae la clave publica asincrona de Clerk y evalua la integridad y caducidad del token.
    """
    if not jwks_client:
        raise HTTPException(status_code=500, detail="Configuracion JWKS ausente en el entorno del servidor.")
    
    token = credentials.credentials
    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            options={"verify_aud": False}
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="El token JWT ha expirado.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Firma de token invalida o malformada.")
    except Exception:
        raise HTTPException(status_code=401, detail="Fallo de autenticacion no controlado.")

@app.get("/api/health")
def health_check():
    return {"status": "ok"}

@app.post("/api/generar", response_model=ResponseData)
def generar_resumen(data: RequestData, session: dict = Depends(validar_token)):
    """
    Endpoint principal protegido. Depende de la resolucion exitosa del middleware de token.
    Implementa el modelo Gemini 1.5 Flash para tareas de generacion rapida de texto.
    """
    if not data.texto.strip():
        raise HTTPException(status_code=400, detail="El payload 'texto' es obligatorio.")
    
    if not genai:
        raise HTTPException(status_code=500, detail="Configuracion de Google Gemini ausente en el servidor.")

    try:
        # Instanciacion del modelo optimizado de Google
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Inyeccion del contexto de sistema directamente en el prompt
        prompt = f"Eres un asistente experto en generar resúmenes concisos de una línea. Resume este texto: {data.texto}"
        
        response = model.generate_content(prompt)
        
        if not response.text:
            raise ValueError("El modelo de IA devolvio una respuesta vacia.")
            
        return ResponseData(resumen=response.text.strip())
        
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error en la resolucion upstream con Gemini: {str(e)}")