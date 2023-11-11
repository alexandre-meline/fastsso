import pytest
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.testclient import TestClient
from unittest.mock import MagicMock

from fastsso.fsapi.core.currentuser import *
from fastsso.fsapi.middleware import KeycloakFastSSOMiddleware

# Our mocked data based on the provided JSON
user_data = {
    "user_id": "647163cb-6dd4-451b-9055-9767aff2cabd",
    "email": "jules.test@gmail.com",
    "first_name": "Jules",
    "last_name": "Malidoi",
    "full_name": "Jules Malidoi",
    "scope": [
        "openid",
        "scopeClientTest",
        "email",
        "profile"
    ],
    "active": True,
    "allowed_origins": [
        "http://localhost:8501/"
    ],
    "resource_access": [
        {
            "microservicebackend1": {
                "roles": [
                    "clientrole"
                ]
            },
            "account": {
                "roles": [
                    "manage-account",
                    "manage-account-links",
                    "view-profile"
                ]
            },
            "microservicefrontend1": {
                "roles": [
                    "Roleclient"
                ]
            }
        }
    ],
    "username": "jules1",
    "email_verified": False,
    "realm_access": {
        "roles": [
            "default-roles-master",
            "offline_access",
            "Premium",
            "uma_authorization"
        ]
    }
}

# Mocking the Request object
class MockUser:
    def __init__(self, data):
        for key, value in data.items():
            setattr(self, key, value)

def mock_request(scope, receive=None, send=None):
    request = Request(scope, receive=receive, send=send)
    request.state.user = MockUser(user_data)
    return request

# Test Application Creation
async def mock_endpoint(request):
    return JSONResponse({"hello": "world"})

app = Starlette(routes=[
    Route("/", mock_endpoint)
])

@app.middleware("http")
async def add_mock_user_to_request(request, call_next):
    request = mock_request(request.scope, request.receive, request.send)
    response = await call_next(request)
    return response

client = TestClient(app)

# Here we begin to define the tests for each function
@pytest.fixture
def test_request():
    with client:
        response = client.get("/")
        return response.request

# Test cases
def test_kc_user(test_request):
    user = kc_user(test_request)
    assert user is not None
    assert user.username == "jules1"

# Similarly, you can create test cases for each function
# You have to adjust the assertions based on the expected values
# and functionalities defined in your functions.

def test_kc_user_id(test_request):
    user_id = kc_user_id(test_request)
    assert user_id == user_data["user_id"]

# ... (create more tests for each function needed)