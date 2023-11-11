from fastapi.testclient import TestClient
import pytest

from tests.fastapiapp import app # 'main' sera changé pour le nom de votre fichier FastAPI
from tests.access_generator import simulate_user_request

client = TestClient(app)

access_token = simulate_user_request("jules1", "password")

@pytest.fixture
def credential_headers():
    # Cette fixture simule l'obtention d'un token auprès de Keycloak pour un utilisateur valide
    # Dans un scénario réel, vous obtiendriez ceci en discutant avec Keycloak 
    # et les détails de l'utilisateur seraient réels et valides.
    headers = {"Authorization": f"Bearer {access_token}"}
    return headers


def test_read_root(credential_headers):
    response = client.get("/", headers=credential_headers)
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == "Hi Jules!" # Assurerez-vous de changer User par le credentials de l'utilisateur de test


def test_realm_user_roles(credential_headers):
    response = client.get("/realm-has-role?role=Premium", headers=credential_headers)
    assert response.status_code == 200
    assert "message" in response.json()
    assert "Premium" in response.json()["message"]
 

def test_get_user_details(credential_headers):
    response = client.get("/user/details/1", headers=credential_headers)
    assert response.status_code == 200
    assert "user_id" in response.json()
    assert "email" in response.json()
    assert "first_name" in response.json()
    assert "last_name" in response.json()
    assert "full_name" in response.json()
    assert "username" in response.json()
    assert "email_verified" in response.json()
    assert "realm_access" in response.json()
    assert "resource_access" in response.json()
    assert "allowed_origins" in response.json()
    assert "active" in response.json()
    