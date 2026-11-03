"""Miniapp resumidora: FastAPI + Gemini + validación de sesión de Clerk."""

import logging
import os
from pathlib import Path

from clerk_backend_api.security import authenticate_request
from clerk_backend_api.security.types import AuthenticateRequestOptions
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from google import genai
from google.genai import types as genai_types
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).resolve().parent

# Carga de variables válida tanto en local (raíz del repositorio) como en Vercel.
load_dotenv(BASE_DIR.parent / ".env")
load_dotenv()

logger = logging.getLogger("miniapp")

app = FastAPI(title="Miniapp IA - Resumidor")

# En Docker, el frontend compilado se copia a api/static. En Vercel no existe:
# la SPA la sirve la plataforma y FastAPI solo atiende /api/*.
STATIC_DIR = Path(os.getenv("STATIC_DIR", BASE_DIR / "static")).resolve()


class RequestData(BaseModel):
    """Entrada del formulario: un único texto acotado para controlar el consumo."""

    texto: str = Field(..., max_length=20_000)


class ResponseData(BaseModel):
    """Contrato de salida estable para el frontend."""

    resumen: str


_client = None


def get_client() -> genai.Client:
    """Crea el cliente de Gemini de forma perezosa, sin fallar al importar."""
    global _client
    if _client is not None:
        return _client

    api_key = os.getenv("AI_PROVIDER_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=503,
            detail="El servicio de IA no está configurado en el servidor.",
        )

    try:
        timeout_seconds = int(os.getenv("AI_TIMEOUT_SECONDS", "30"))
    except ValueError:
        logger.warning("AI_TIMEOUT_SECONDS no es un número; se usan 30 segundos.")
        timeout_seconds = 30

    timeout_ms = max(timeout_seconds, 1) * 1000
    _client = genai.Client(
        api_key=api_key,
        http_options=genai_types.HttpOptions(timeout=timeout_ms),
    )
    return _client


def _authorized_parties() -> list[str] | None:
    """Orígenes permitidos para el claim azp de Clerk (separados por comas)."""
    raw = os.getenv("CLERK_AUTHORIZED_PARTIES", "")
    parties = [party.strip() for party in raw.split(",") if party.strip()]
    return parties or None


def require_user(request: Request) -> dict:
    """Valida el JWT de Clerk enviado en `Authorization: Bearer ...`.

    La comprobación se delega en el SDK oficial: firma, caducidad, `nbf`,
    `azp` y resto de parámetros aplicables a la instancia de Clerk.
    """
    authorization = request.headers.get("authorization", "")
    if not authorization.lower().startswith("bearer "):
        raise HTTPException(
            status_code=401,
            detail="Sesión no válida o ausente.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    secret_key = os.getenv("CLERK_SECRET_KEY")
    if not secret_key:
        logger.error("CLERK_SECRET_KEY no está configurada en el servidor.")
        raise HTTPException(
            status_code=503,
            detail="La autenticación no está configurada en el servidor.",
        )

    authorized_parties = _authorized_parties()
    if not authorized_parties:
        logger.warning(
            "CLERK_AUTHORIZED_PARTIES no está configurado; no se valida el claim azp."
        )

    try:
        state = authenticate_request(
            request,
            AuthenticateRequestOptions(
                secret_key=secret_key,
                authorized_parties=authorized_parties,
                # Solo sesiones de usuario: no se aceptan claves de API ni tokens de máquina.
                accepts_token=["session_token"],
            ),
        )
    except Exception:
        logger.exception("Error al validar el token de Clerk.")
        raise HTTPException(
            status_code=401,
            detail="Sesión no válida o ausente.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not state.is_signed_in:
        logger.info("Token de Clerk rechazado: %s", state.reason)
        raise HTTPException(
            status_code=401,
            detail="Sesión no válida o ausente.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return state.payload or {}


@app.get("/api/health")
def health_check():
    """Comprobación pública de disponibilidad; no revela información sensible."""
    return {"status": "ok"}


@app.post("/api/generar", response_model=ResponseData)
def generar_resumen(data: RequestData, _user: dict = Depends(require_user)):
    """Resume el texto recibido mediante Gemini. Requiere sesión de Clerk válida."""
    texto = data.texto.strip()
    if not texto:
        raise HTTPException(status_code=400, detail="El campo 'texto' es obligatorio.")

    client = get_client()
    prompt = (
        "Eres un asistente que resume textos de forma clara y breve. "
        "Devuelve un único párrafo de una o dos frases, sin introducciones. "
        f"Texto a resumir:\n\n{texto}"
    )

    try:
        response = client.models.generate_content(
            model=os.getenv("AI_MODEL", "gemini-2.5-flash"),
            contents=prompt,
        )
    except Exception:
        # El detalle se registra en el servidor; al cliente solo va un mensaje genérico.
        logger.exception("Fallo al llamar al proveedor de IA.")
        raise HTTPException(
            status_code=502,
            detail="No se pudo obtener el resumen del proveedor de IA.",
        )

    resumen = getattr(response, "text", None)
    if not resumen or not resumen.strip():
        logger.error("El proveedor de IA devolvió una respuesta vacía.")
        raise HTTPException(
            status_code=502,
            detail="El proveedor de IA devolvió una respuesta vacía.",
        )

    return ResponseData(resumen=resumen.strip())


if STATIC_DIR.is_dir():
    assets_dir = STATIC_DIR / "assets"
    if assets_dir.is_dir():
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.get("/{full_path:path}", include_in_schema=False)
    def spa_fallback(full_path: str):
        """Sirve la SPA compilada y deja que React resuelva las rutas del cliente."""
        if full_path.startswith("api/"):
            raise HTTPException(status_code=404, detail="Not Found")

        candidate = (STATIC_DIR / full_path).resolve() if full_path else None
        if candidate and candidate.is_file() and STATIC_DIR in candidate.parents:
            return FileResponse(candidate)

        index = STATIC_DIR / "index.html"
        if index.is_file():
            return FileResponse(index)

        raise HTTPException(status_code=404, detail="Not Found")
