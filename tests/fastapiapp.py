from fastapi import FastAPI, Request, HTTPException
from typing import List, Optional
from dotenv import load_dotenv
import os

# Keycloak Fast SSO imports
# Middleware for protecting endpoints {REQUIRED}
from fastsso.fsapi.middleware import KeycloakFastSSOMiddleware
# Decorators for protecting endpoints {OPTIONAL}
from fastsso.fsapi.decorators import (require_realm_roles,
                                    require_realm_roles,
                                    require_scope,
                                    require_email_verified,
                                    require_active_user,
                                    require_allowed_origin,
                                    require_resource_access
                                    )

# Functions to get user information from request state {OPTIONAL}
from fastsso.fsapi.core.currentuser import *
# Basic unprotected endpoint not requiring authentication {OPTIONAL} 
from fastsso.fsapi.utils.unprotected_endpoints import get_all_endpoints, unprotected_basic_endpoint

load_dotenv('.env.test')
BACKEND_SERVER_URL = os.getenv("BACKEND_SERVER_URL")
BACKEND_CLIENT_ID = os.getenv("BACKEND_CLIENT_ID")
BACKEND_REALM_NAME = os.getenv("BACKEND_REALM_NAME")
BACKEND_CLIENT_SECRET_KEY = os.getenv("BACKEND_CLIENT_SECRET_KEY")

app = FastAPI()

# Add Keycloak Fast SSO middleware in FastAPI app
# Now all endpoints are protected by default and require token validation
# except endpoints in unprotected_basic_endpoint
# If you want to protect all endpoints, just remove unprotected_basic_endpoint
# If you want to protect only some endpoints, just add them in unprotected_basic_endpoint
# unprotected_basic_endpoint = ["/docs", "/openapi.json", "/redoc"]

app.add_middleware(KeycloakFastSSOMiddleware, server_url=BACKEND_SERVER_URL, 
                                            client_id=BACKEND_CLIENT_ID,
                                            realm_name=BACKEND_REALM_NAME, 
                                            client_secret_key=BACKEND_CLIENT_SECRET_KEY,
                                            unprotected_endpoints=unprotected_basic_endpoint,
                                            user_model=None, create_user=False)

# _________________________________________________________________ #
#                                                                   #
#                       UNPROTECTED ENDPOINTS                       #
#                     JUST BEARER TOKEN REQUIRE                     #
#                                                                   #
# _________________________________________________________________ #

# Unprotected endpoint
@app.get("/")
def read_root(request: Request):
    return {"message": f"Hi {kc_user_first_name(request)}!"}


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
def realm_has_role(request: Request, role: str = "Premium"):
    """
    Checks if user has a specific role in the realm.
    
    Args:
        request (`Request`): The request the user wants to check authentication status for.
        
    Returns:
        bool: True if request is authenticated, False otherwise.
    """
    # Check if user has role
    has_role = kc_realm_has_role(request, role=role)

    # If user has role
    if has_role:
        return {"message": f"User has role {role}"}
    # If user does not have role
    else:
        return {"message": f"User does not have role {role}"}


# Endpoint to get the authenticated user's detailed information
@app.get("/user/details/1")
def get_user_details(request: Request):
    """
    An endpoint to retrieve the full details of the authenticated user.
    Requires an authenticated request.
    """

    user_details = {
        "user_id": kc_user_id(request),
        "email": kc_user_email(request),
        "first_name": kc_user_first_name(request),
        "last_name": kc_user_last_name(request),
        "full_name": kc_user_full_name(request),
        "scope": kc_user_scope(request),
        "active": kc_active_user(request),
        "allowed_origins": kc_user_allowed_origins(request),
        "resource_access": kc_user_resource_access(request),
        "username": kc_username(request),
        "email_verified": kc_user_verified_email(request),
        "realm_access": kc_realm_access(request)
    }
    return user_details

@app.get("/user/details/2")
def get_user_details(request: Request):
    """
    An endpoint to retrieve the full details of the authenticated user.
    Requires an authenticated request.
    """

    user_details = {
        "user_id": request.state.user.id,
        "email": request.state.user.email,
        "first_name": request.state.user.given_name,
        "last_name": request.state.user.family_name,
        "full_name": request.state.user.name,
        "scope": request.state.user.scope,
        "active": request.state.user.active,
        "allowed_origins": request.state.user.allowed_origins,
        "resource_access": request.state.user.resource_access,
        "username": request.state.user.preferred_username,
        "email_verified": request.state.user.email_verified,
        "realm_access": request.state.user.realm_access
    }
    return user_details

# Endpoint to check user's role
@app.get("/user/has-role/{required_role}")
def check_user_role(request: Request, required_role: str):
    """
    An endpoint to check if the current user has a specific role.
    The role to check is provided as a path parameter 'required_role'.
    Requires an authenticated request with roles included.
    """
    print(request.state.user.realm_roles)
    has_role = kc_realm_has_role(request, required_role)
    return {"has_role": has_role}


print(get_all_endpoints(app))