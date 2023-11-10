
<p align="center">
  <img src="/docs/keycloakfastsso.png" alt="keycloakfastsso"/>
</p>

![PyPI - License](https://img.shields.io/pypi/l/Keycloak-fast-sso)
![PyPI - Version](https://img.shields.io/pypi/v/keycloak-fast-sso)
![GitHub commit activity (branch)](https://img.shields.io/github/commit-activity/t/alexandre-meline/keycloakfastsso)
![CodeFactor Grade](https://img.shields.io/codefactor/grade/github/alexandre-meline/keycloakfastsso)


# fast-sso

`fastsso` is a Python package that facilitates the integration of Keycloak authentication in applications built with the FastAPI web framework.

## Features 🎁

- Authentication with bearer JWT tokens.
- JWT token validation.
- Authorization based on roles, groups and the user's email verification state in Keycloak.
- Provides information about the validated user.
- Handy tools for checking roles, groups and other user attributes.

## Usage 💡

### Middleware
Use KeycloakFastSSOMiddleware to protect your API routes. You must first configure the connection to Keycloak with the appropriate parameters.

```python
from fastapi import FastAPI
from keycloakfastsso.middleware import KeycloakFastSSOMiddleware

app = FastAPI()
app.add_middleware( KeycloakFastSSOMiddleware,
                    server_url="https://my-keycloak-url/auth/",
                    client_id="my-client-id",
                    realm_name="my-realm-name",
                    client_secret_key="my-client-secret-key")
```
### Decorators 

These decorators can be used to restrict access to routes based on user roles or groups.

```python
from keycloakfastsso.decorators import require_role, require_group, require_scope, require_email_verified, require_active_user, require_token_type, require_resource_access, require_allowed_origin

@app.get("/require_role")
@require_role(["admin"])
def require_role_endpoint(): 
    return {"Hello": "World"}

@app.get("/require_group")
@require_group(["my_group"])
def require_group_endpoint(): 
    return {"Hello": "World"}

# other routes continue the same way 
```
### Utilities

The utilities allow you to retrieve specific information about the currently authenticated user.

```python
from keycloakfastsso.utils import KeycloakUtils

# In your route
@app.get("/whoami")
def who_am_i(request: Request):
    return {"user_id": KeycloakUtils.get_user_id(request)}
```

## Installation 🛠️

You can install `keycloakfastsso` with pip:

```bash
pip install keycloak-fast-sso
```

---

For more information on how to use this package, please refer to the official documentation.
  1. [FastAPI avec Keycloak Fast SSO](https://medium.com/@alexandre.ml/introduction-%C3%A0-keycloak-et-keycloak-fast-sso-76b81fc4572d)
