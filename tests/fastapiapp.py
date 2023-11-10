from fastapi import FastAPI, Request, HTTPException
from typing import List, Optional

# Keycloak Fast SSO imports
# Middleware for protecting endpoints {REQUIRED}
from fastsso.fastapi.middleware import KeycloakFastSSOMiddleware
# Decorators for protecting endpoints {OPTIONAL}
from fastsso.fastapi.decorators import *
# Logger for debugging purposes {OPTIONAL}
from fastsso.fastapi.logging import logger
# Functions to get user information from request state {OPTIONAL}
from fastsso.fastapi.core.currentuser import *
# Basic unprotected endpoint not requiring authentication {OPTIONAL} 
from fastsso.fastapi.utils.unprotected_endpoints import unprotected_basic_endpoint

logger.info("Starting the FastAPI server")

app = FastAPI()

# Ajoutez une configuration ici (server_url, client_id, etc.).
app.add_middleware(KeycloakFastSSOMiddleware,   server_url='http://localhost:8080/', 
                                                client_id='microservicebackend1', realm_name='master', 
                                                client_secret_key='vzqJpMYa3CiO5VGXkd20q7tOebrsDsP1',
                                                unprotected_endpoints=unprotected_basic_endpoint,
                                                user_model=None, create_user=False)

#@require_role(roles=["banal-users"])
#@require_scope(scopes=["openid profile email"])
#@require_email_verified
#@require_active_user
#@require_token_type(token_type="Bearer")
#@require_resource_access(resource="frontend", role="banal-users")
#@require_allowed_origin(origin="http://localhost:8001/")


# Unprotected endpoint
@app.get("/")
def read_root(request: Request):
    #user = kc_user(request)
    firstname = request.state.user.given_name
    return {"message": f"Hi {firstname}!"}


# Unprotected endpoint
@app.get("/user")
def user(request: Request):
    user = kc_user(request)
    return {"user": user}


# Unprotected endpoint
@app.get("/user-get-info")
def user_firstname(request: Request, user_info: str = "given_name"):

    # 2 solutions for getting user info

    # _ Solution 1: Use kc_get_user_info function
    firstname = kc_get_user_info(request, user_info)

    # _ Solution 2: Use request.state.user object
    #firstname = request.state.user.given_name

    return {"user": firstname}


# Unprotected endpoint
@app.get("/realm-has-role")
def realm_has_role(request: Request):
    """
    Checks if user has a specific role in the realm.
    
    Args:
        request (`Request`): The request the user wants to check authentication status for.
        
    Returns:
        bool: True if request is authenticated, False otherwise.
    """
    # Set role
    role = "Premium"
    # Check if user has role
    has_role = kc_realm_has_role(request, role=role)

    # If user has role
    if has_role:
        return {"message": f"User has role {role}"}
    # If user does not have role
    else:
        return {"message": f"User does not have role {role}"}


