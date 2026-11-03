"""Tests de comportamiento del backend: proveedor simulado y sesión de Clerk."""

from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient
from google.genai import errors as genai_errors

import main

client = TestClient(main.app)


@pytest.fixture(autouse=True)
def _limpiar_overrides():
    """Aísla cada test de las dependencias sobrescritas por el anterior."""
    main.app.dependency_overrides.clear()
    yield
    main.app.dependency_overrides.clear()


class _FakeModels:
    def __init__(self, error=None, fail_models=None):
        self.error = error
        self.fail_models = set(fail_models or ())
        self.calls = []

    def generate_content(self, model, **_kwargs):
        self.calls.append(model)
        if model in self.fail_models:
            raise genai_errors.ServerError(
                503,
                {"error": {"code": 503, "message": "high demand"}},
            )
        if self.error:
            raise self.error
        return SimpleNamespace(text="Resumen de prueba.")


class _FakeClient:
    def __init__(self, error=None, fail_models=None):
        self.models = _FakeModels(error, fail_models)


def _permitir_sesion() -> None:
    """Sustituye la dependencia de Clerk para aislar el resto del endpoint."""
    main.app.dependency_overrides[main.require_user] = lambda: {"sub": "user_test"}


def test_health_check_es_publico():
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_generar_resumen_con_sesion_valida(monkeypatch):
    monkeypatch.setenv("CLERK_SECRET_KEY", "sk_test_dummy")
    monkeypatch.setattr(
        main,
        "authenticate_request",
        lambda _request, _options: SimpleNamespace(
            is_signed_in=True,
            payload={"sub": "user_test"},
        ),
    )
    monkeypatch.setattr(main, "get_client", lambda: _FakeClient())

    response = client.post(
        "/api/generar",
        json={"texto": "Texto de entrada válido para la prueba."},
        headers={"Authorization": "Bearer token-de-prueba"},
    )

    assert response.status_code == 200
    assert response.json() == {"resumen": "Resumen de prueba."}


def test_generar_usa_modelo_de_respaldo_si_el_primario_esta_saturado(monkeypatch):
    _permitir_sesion()
    monkeypatch.setenv("AI_MODEL", "gemini-2.5-flash")
    monkeypatch.setenv("AI_FALLBACK_MODEL", "gemini-3.5-flash")
    fake = _FakeClient(fail_models={"gemini-2.5-flash"})
    monkeypatch.setattr(main, "get_client", lambda: fake)

    response = client.post("/api/generar", json={"texto": "Texto válido."})

    assert response.status_code == 200
    assert response.json() == {"resumen": "Resumen de prueba."}
    assert fake.models.calls == ["gemini-2.5-flash", "gemini-3.5-flash"]


def test_generar_devuelve_503_si_todos_los_modelos_estan_saturados(monkeypatch):
    _permitir_sesion()
    monkeypatch.setenv("AI_MODEL", "gemini-2.5-flash")
    monkeypatch.setenv("AI_FALLBACK_MODEL", "gemini-3.5-flash")
    fake = _FakeClient(
        fail_models={"gemini-2.5-flash", "gemini-3.5-flash"}
    )
    monkeypatch.setattr(main, "get_client", lambda: fake)

    response = client.post("/api/generar", json={"texto": "Texto válido."})

    assert response.status_code == 503
    assert "saturado" in response.json()["detail"].lower()
    assert "high demand" not in response.text
    assert fake.models.calls == ["gemini-2.5-flash", "gemini-3.5-flash"]


def test_generar_rechaza_texto_vacio():
    _permitir_sesion()

    response = client.post("/api/generar", json={"texto": "   "})

    assert response.status_code == 400
    assert "texto" in response.json()["detail"].lower()


def test_generar_devuelve_502_si_falla_el_proveedor(monkeypatch):
    _permitir_sesion()
    monkeypatch.setattr(
        main,
        "get_client",
        lambda: _FakeClient(error=RuntimeError("detalle interno del proveedor")),
    )

    response = client.post("/api/generar", json={"texto": "Texto válido."})

    assert response.status_code == 502
    assert "detalle interno" not in response.text
    assert "proveedor" in response.json()["detail"].lower()


def test_generar_rechaza_peticion_sin_token():
    response = client.post("/api/generar", json={"texto": "Texto válido."})

    assert response.status_code == 401
    assert "sesión" in response.json()["detail"].lower()


def test_generar_rechaza_token_invalido(monkeypatch):
    monkeypatch.setenv("CLERK_SECRET_KEY", "sk_test_dummy")
    monkeypatch.setattr(
        main,
        "authenticate_request",
        lambda _request, _options: SimpleNamespace(
            is_signed_in=False,
            reason="token-invalid",
        ),
    )

    response = client.post(
        "/api/generar",
        json={"texto": "Texto válido."},
        headers={"Authorization": "Bearer token-invalido"},
    )

    assert response.status_code == 401
    assert "sesión" in response.json()["detail"].lower()
