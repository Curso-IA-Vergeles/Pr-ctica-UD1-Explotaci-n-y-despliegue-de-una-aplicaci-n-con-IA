import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app

test_client = TestClient(app)

def test_health_check_returns_200():
    """Valida la disponibilidad del endpoint de monitorización."""
    response = test_client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_generar_resumen_rejects_empty_payload():
    """Valida que el controlador HTTP rechace entradas en blanco con código 400."""
    response = test_client.post("/api/generar", json={"texto": "   "})
    assert response.status_code == 400

@patch("main.client")
def test_generar_resumen_successful_mock(mock_openai_client):
    """
    Valida el flujo principal interceptando la llamada a OpenAI.
    Evita latencia de red y gastos operativos en la canalización de CI/CD.
    """
    # Configuración del objeto mock para emular la estructura de respuesta anidada de OpenAI
    mock_message = type("obj", (object,), {"content": "Resumen generado por el mock."})
    mock_choice = type("obj", (object,), {"message": mock_message})
    mock_response = mock_openai_client.chat.completions.create.return_value
    mock_response.choices = [mock_choice]
    
    response = test_client.post("/api/generar", json={"texto": "Texto de entrada válido para la prueba."})
    
    assert response.status_code == 200
    assert response.json() == {"resumen": "Resumen generado por el mock."}