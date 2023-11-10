"""
MIT License

Copyright (c) 2023 Alexandre Meline <alexandre.meline.dev@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Type, List, Dict, Optional
from pydantic import BaseModel

# KecloakFastSSO
from fastsso.fastapi.utils.keycloak_validator import keycloakValidator
from fastsso.fastapi.utils.user import User, get_user_info
from fastsso.fastapi.core.exceptions import (unauthorized_response,
                                                    invalid_token_response,
                                                    unverified_user_response,
                                                    keycloak_server_not_up_response,
                                                    keycloak_middleware_failed_response)

class KeycloakFastSSOMiddleware(BaseHTTPMiddleware):
    """
    This is a middleware class for integrating Keycloak with FastAPI for Single-Sign-On (SSO) Authentication. 
    Any incoming requests will be passed through this middleware to check for the necessary authentication details
    provided by Keycloak.
    
    This class also offers optional functionalities related to User Model initialization and to user verification.
    """

    def __init__(self, app, server_url: str,
                             client_id: str,
                             realm_name: str,
                             client_secret_key: str,
                             custom_headers: dict = None,
                             proxies: dict = None,
                             timeout: int = None,
                             # Additional parameters
                             unprotected_endpoints: Optional[List[str]] = [], # List of unprotected endpoints (optional)
                             user_model: Optional[Type[BaseModel]] = None, # User model class for creating user from token informations (optional)
                             create_user:  Optional[bool] = False, # Flag to decide if creating user is allowed (optional)
                        ):
        """
        Constructor for KeycloakFastSSOMiddleware class. 
        Initializes Keycloak middleware and checks if middleware was initialized successfully.

        Args:
            app (`obj`): The instantiated FastAPI application.
            server_url (`str`): The URL to Keycloak server.
            client_id (`str`): The client ID of the Keycloak client.
            realm_name (`str`): The realm name of the Keycloak server.
            client_secret_key (`str`): The client secret key provided by Keycloak server for authentication.
            user_model (`obj`, optional): User model class. Defaults to None.
            create_user (`bool`, optional): Flag to decide if creating user is allowed. Defaults to False.
            enable_user_verification (`bool`, optional): Flag to decide if user's email verification is enabled or not.
                                                            Defaults to False.

        Raises:
            Exception: Raises an exception if failed to initialize the Keycloak middleware.
        """
        super().__init__(app)
        # Init Keycloak validator in current class object
        self.keycloak_validator = None

        try:
            # Try to initialize Keycloak validator
            keycloak_validator = keycloakValidator(server_url=server_url,
                                                    client_id=client_id,
                                                    realm_name=realm_name,
                                                    client_secret_key=client_secret_key)
            # Check if Keycloak server is up
            if keycloak_validator.keycloak_validate_connection():
                # Set Keycloak validator in current class object
                setattr(self, 'keycloak_validator', keycloak_validator)
            else:
                return keycloak_server_not_up_response()

        except Exception as _:
            return keycloak_middleware_failed_response()

        self.unprotected_endpoints = unprotected_endpoints
        self.user_model = user_model
        self.create_user = create_user


    async def dispatch(self, request, call_next):
        """
        Async function that processes incoming HTTP request and
        if necessary verifies the user.

        Args:
            request (`obj`): The incoming HTTP request
            call_next (`obj`): The middleware to be launched after this one

        Returns:
            `obj`: Returns the response that was created by this middleware or 
            in case of failed authentication, return respective HTTPException.

        Raises:
            HTTPException: If user verification failed.
        """
        # Init Authorization header and token
        authorization_header = None
        token = None
        
        # Check if endpoint is unprotected or not requiring authentication
        if request.url.path in self.unprotected_endpoints:
            return await call_next(request)
        
        # Try to get token from headers in request object if it exists otherwise return unauthorized response
        try:
            # Get authorization header
            authorization_header = request.headers.get('Authorization')
            # Get token from authorization header
            if authorization_header:
                # Split token from bearer
                scheme, token = authorization_header.split()
                # Check if token is bearer token in contexte no interact with user directly
                if scheme.lower() != "bearer":
                    return unauthorized_response()
            else:
                return unauthorized_response()
        except Exception as _:
            return unauthorized_response()
        
        # Get token info
        token_info = self.keycloak_validator.token_to_user_info(token)
        # Check if token is valid
        if not token_info:
            return invalid_token_response()
        # Get user info from token and set request state for future use
        self.set_request_state(request, token=token_info)

        return await call_next(request)

    
    def set_request_state(self, request, token: str = None):
        """
        Update the state of the given request with information extracted from the token.
        
        Args:
            request (`obj`): The incoming request.
        """
        # Add user representation informations to request state
        request.state.user = get_user_info(token)