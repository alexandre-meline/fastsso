# KeycloakFastSSOMiddleware

The `KeycloakFastSSOMiddleware` is a middleware for integrating Keycloak with FastAPI for Single Sign-On (SSO) authentication. It ensures that incoming requests are authenticated, and provides utility functions for accessing user information.

## Usage

To use `KeycloakFastSSOMiddleware`, you need to add it to your FastAPI application upon creation. You also need to provide necessary configurations such as `server_url`, `client_id`, `realm_name`, etc.

### Example

```python
from fastapi import FastAPI
from fastsso.fsapi.middleware import KeycloakFastSSOMiddleware

app = FastAPI()

app.add_middleware(KeycloakFastSSOMiddleware,
                   server_url="https://keycloak.example.com/",
                   client_id="your-client-id",
                   realm_name="your-realm",
                   client_secret_key="your-client-secret",
                   # Optionally configuration
                   unprotected_endpoints=["/health", "/metrics"],
                   user_model=YourUserModel,
                   create_user=True)
```

## Parameters

- `app`: Your FastAPI application instance.
- `server_url`: The URL where the Keycloak server is accessible.
- `client_id`: The client ID configured within the Keycloak realm.
- `realm_name`: The name of the Keycloak realm.
- `client_secret_key`: The client's secret key provided by Keycloak for authentication.
- `unprotected_endpoints` (optional): A list of API endpoint paths that do not require authentication.
- `user_model` (optional): A Pydantic model class that represents a user.
- `create_user` (optional): A boolean that enables automatic user creation within your application based on Keycloak tokens.

## Methods

- `dispatch`: An async method that processes incoming HTTP requests and performs authentication checks.
- `set_request_state`: A method used internally to update the state of a given request with user information after successful authentication.

## How It Works

When a request is made to your FastAPI application, the `KeycloakFastSSOMiddleware` checks the `Authorization` header for a valid Keycloak token. If the token is valid, it extracts user information and adds it to the `state` attribute of the request object. Requests to unprotected endpoints specified in the configuration are passed through without authorization checks.

You can access the authenticated user's information from your API endpoint functions using the current user utility functions provided:

```python
from fastapi import Depends
from fastsso.fsapi.core.currentuser import kc_user

@app.get("/user")
async def get_user(user=Depends(kc_user)):
    return user
```