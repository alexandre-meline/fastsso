import json
from starlette.requests import Request


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
    return request.state.user if kc_user_is_authenticated(request) else None



def kc_user_is_authenticated(request: Request):
    """
    Returns a flag indicating whether the request is authenticated or not.

    Args:
        request (`Request`): The request the user wants to check authentication status for.

    Returns:
        bool: True if request is authenticated, False otherwise.

    Example:
        >>> kc_user_is_authenticated(request)
        True
    """
    return bool(request.state.user.active)


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
    user_info = request.state.user.__dict__.get(attr) if kc_user_is_authenticated(request) else None
    return user_info if kc_user_is_authenticated(request) else None


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
    realm_roles = request.state.user.realm_roles
    return role in realm_roles if kc_user_is_authenticated(request) else False

'''
def kc_user_in_group(request: Request, group: str):
    """
    Checks the request if the user is in the specified group.

    Args:
        request (`Request`): The request to check if a user is in a group.
        group (`str`): The group to check if the user is a member of.

    Returns:
        bool: True if user is in specified group, False otherwise.
    
    Example:
        >>> is_in_group(request, "test_group")
        False
    """
    groups = request.state.token_info.get('groups', [])
    return group in groups if kc_user_is_authenticated(request) else False


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
    user_id = request.state.token_info.get('sub') if kc_user_is_authenticated(request) else None
    return user_id if kc_user_is_authenticated(request) else None


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
    user_email = request.state.token_info.get('email') if kc_user_is_authenticated(request) else None
    return user_email if kc_user_is_authenticated(request) else None


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
    user_first_nm = request.state.token_info.get('given_name') if kc_user_is_authenticated(request) else None
    return user_first_nm if kc_user_is_authenticated(request) else None


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
    user_last_nm = request.state.token_info.get('family_name') if kc_user_is_authenticated(request) else None
    return user_last_nm if kc_user_is_authenticated(request) else None


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
    user_full_name = request.state.token_info.get('name') if kc_user_is_authenticated(request) else None
    return user_full_name if kc_user_is_authenticated(request) else None


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
    scope = request.state.user_scope
    return scope if kc_user_is_authenticated(request) else None


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
    user_verif = request.state.token_info.get('email_verified') if kc_user_is_authenticated(request) else None
    return user_verif if kc_user_is_authenticated(request) else None


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
    active_user = request.state.token_info.get('active') if kc_user_is_authenticated(request) else None
    return active_user if kc_user_is_authenticated(request) else None


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
    rsc_acs = request.state.token_info.get('resource_access') if kc_user_is_authenticated(request) else None
    return rsc_acs if kc_user_is_authenticated(request) else None
'''