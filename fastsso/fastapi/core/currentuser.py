"""
MIT License

Copyright (c) 2023 Alexandre Meline <alexandre[.]meline[.]dev[@]gmail.com>

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
from starlette.requests import Request


def _kc_user_is_authenticated(request: Request):
    """
    Returns a flag indicating whether the request is authenticated or not.

    Args:
        request (`Request`): The request the user wants to check authentication status for.

    Returns:
        bool: True if request is authenticated, False otherwise.

    Example:
        >>> _kc_user_is_authenticated(request)
        True
    """
    return bool(request.state.user.active)
    

def kc_user(request: Request):
    """
    Returns the user object from the authenticated request.

    Args:
        request (`Request`): The request the user wants to get the info from.

    Returns:
        `dict`: The user object of the authenticated user.

    Example:
        >>> kc_user(request)
        {
            "sub": "123456",
            "email_verified": True,
            "name": "John Smith",
            "preferred_username": "john.smith",
            "given_name": "John",
            "family_name": "Smith",
            "email": "john.smith@email.com"
            "email_verified": True,
            "realm_access": {
                "roles": [
                    "offline_access",
                    "uma_authorization"
                ]
            },
            "resource_access": {
                "account": {
                    "roles": [""]
                }
                "backend": {
                    "roles": [
                        "prenium-user"
                    ]
                }
            }
            "active": True,
            "scope": "openid profile email",
            "client_id": "backend",
            "allowed-origins": [
                "http://localhost:8000/"
            ]
        }
    """
    return request.state.user if _kc_user_is_authenticated(request) else None


def kc_get_user_info(request: Request, attr: str):
    """
    Returns the user info for a given attribute from the authenticated request.

    Args:
        request (`Request`): The request the user wants to get the info from.
        attr (`str`): The attribute the user wants to get the info for.

    Returns:
        `str`: The info of the user for the given attribute.

    Example:
        >>> get_user_info(request, "name")
        'John Smith'
    """
    return getattr(request.state.user, attr) if _kc_user_is_authenticated(request) else None


def kc_realm_access(request: Request):
    """
    Returns the realm access of the authenticated user from the request state.

    Args:
        request: The incoming server request.

    Returns:
        The realm access of the user authenticated via Keycloak if authenticated, else None.
        
    Examples:
        realm_access = get_realm_access(request)
    """
    return request.state.user.realm_access if _kc_user_is_authenticated(request) else None


def kc_realm_has_role(request: Request, role: str):
    """
    Checks the request if the user has the specified role in realm.

    Args:
        request (`Request`): The request where to extract user's roles.
        role (`str`): The role to check if the user has.

    Returns:
        bool: True if user has specified role, False otherwise.

    Example:
        >>> has_role(request, "admin")
        True
    """
    print(role)
    return role if role in request.state.user.realm_roles else None

def kc_user_id(request: Request):
    """
    Returns the user id from the authenticated request.

    Args:
        request (`Request`): The request which carries user's details.

    Returns:
        str: The user id of the authenticated user.

    Example:
        >>> get_user_id(request)
        '123456'
    """
    return request.state.user.id if _kc_user_is_authenticated(request) else None


def kc_user_email(request: Request):
    """
    Returns the user's email from the authenticated request.

    Args:
        request (`Request`): The request which carries user's details.

    Returns:
        str: The email of the authenticated user.

    Example:
        >>> get_user_email(request)
        'user@example.com'
    """
    return request.state.user.email if _kc_user_is_authenticated(request) else None


def kc_user_first_name(request: Request):
    """
    Extracts the first name ('given_name') of the authenticated user from the request state.

    Args:
        request: The incoming server request.

    Returns:
        The first name of the user authenticated via Keycloak if authenticated, else None.
        
    Examples:
        first_name = get_user_first_name(request)
    """
    return request.state.user.given_name if _kc_user_is_authenticated(request) else None


def kc_user_last_name(request: Request):
    """
    Extracts the last name ('family_name') of the authenticated user from the request state.

    Args:
        request: The incoming server request.

    Returns:
        The last name of the user authenticated via Keycloak if authenticated, else None.
        
    Examples:
        last_name = get_user_last_name(request)
    """
    return request.state.user.family_name if _kc_user_is_authenticated(request) else None


def kc_user_full_name(request: Request):
    """
    Extracts the full name ('name') of the authenticated user from the request state.

    Args:
        request: The incoming server request.

    Returns:
        The full name of the user authenticated via Keycloak if authenticated, else None.
        
    Examples:
        full_name = get_user_full_name(request)
    """
    return request.state.user.name if _kc_user_is_authenticated(request) else None


def kc_user_scope(request: Request):
    """
    Extracts the scope of the authenticated user from the request state.

    Args:
        request: The incoming server request.

    Returns:
        The scope of the user authenticated via Keycloak if authenticated, else None.
        
    Examples:
        scope = get_scope(request)
    """
    return request.state.user.scope if _kc_user_is_authenticated(request) else None


def kc_user_verified_email(request: Request):
    """
    Extracts the verification status ('email_verified') of the authenticated user from the request state.

    Args:
        request: The incoming server request.

    Returns:
        The verification status of the user authenticated via Keycloak if authenticated, else None.
        
    Examples:
        is_verified = get_user_verified(request)
    """
    return request.state.user.email_verified if _kc_user_is_authenticated(request) else None


def kc_active_user(request: Request):
    """
    Extracts the activity status ('active') of the authenticated user from the request state.

    Args:
        request: The incoming server request.

    Returns:
        The activity status of the user authenticated via Keycloak if authenticated, else None.
        
    Examples:
        is_active = get_active_user(request)
    """
    return request.state.user.active if _kc_user_is_authenticated(request) else None


def kc_user_resource_access(request: Request):
    """
    Extracts the resource access details of the authenticated user from the request state.

    Args:
        request: The incoming server request.

    Returns:
        The resource access details of the user authenticated via Keycloak if authenticated, else None.
        
    Examples:
        resource_access = get_resource_access(request)
    """
    return request.state.user.resource_access


def kc_username(request: Request):
    """
    Extracts the username of the authenticated user from the request state.

    Args:
        request: The incoming server request.

    Returns:
        The username of the user authenticated via Keycloak if authenticated, else None.
        
    Examples:
        username = get_username(request)
    """
    return request.state.user.preferred_username if _kc_user_is_authenticated(request) else None


def kc_user_allowed_origins(request: Request):
    """
    Extracts the allowed origins of the authenticated user from the request state.

    Args:
        request: The incoming server request.

    Returns:
        The allowed origins of the user authenticated via Keycloak if authenticated, else None.
        
    Examples:
        allowed_origins = get_allowed_origins(request)
    """
    return request.state.user.allowed_origins


def kc_user_resource_access(request: Request):
    """
    Extracts the resource access details of the authenticated user from the request state.

    Args:
        request: The incoming server request.

    Returns:
        The resource access details of the user authenticated via Keycloak if authenticated, else None.
        
    Examples:
        resource_access = get_resource_access(request)
    """
    return request.state.user.resource_access  