from keycloak import KeycloakOpenID
from dotenv import load_dotenv
import os

load_dotenv('.env.test')

SERVER_URL = os.environ.get("SERVER_URL")
CLIENT_ID = os.environ.get("CLIENT_ID")
REALM_NAME = os.environ.get("REALM_NAME")
CLIENT_SECRET_KEY = os.environ.get("CLIENT_SECRET_KEY")

# Configure client
keycloak_openid = KeycloakOpenID(server_url=SERVER_URL,
                                 client_id=CLIENT_ID,
                                 realm_name=REALM_NAME,
                                 client_secret_key=CLIENT_SECRET_KEY)
# Check if server is up
try:
    keycloak_openid.well_known()
except:
    print("Error: Keycloak server is not available")
    exit(1)


# _________________ Frontend simulated user request to backend _________________ #


# Function simulate a request from frontend to backend with token in header
def simulate_user_request(username: str, password: str):
    # Get Token
    token = keycloak_openid.token(username, password)
    if 'access_token' in token:
        return token['access_token']

    return None


print(simulate_user_request("jules1", "password"))