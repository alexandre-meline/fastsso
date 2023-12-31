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

from functools import wraps
from starlette.responses import JSONResponse
from fastapi import Request
from typing import List
from fastsso.fsapi.core.currentuser import (  kc_user,
                                                kc_get_user_info,
                                                kc_realm_access,
                                                kc_realm_has_role,
                                                kc_user_id,
                                                kc_user_email,
                                                kc_user_first_name,
                                                kc_user_last_name,
                                                kc_user_full_name,
                                                kc_user_scope,
                                                kc_user_verified_email,
                                                kc_active_user,
                                                kc_user_resource_access,
                                                kc_username,
                                                kc_user_allowed_origins,
                                                kc_user_resource_access
                                              )

def require_realm_roles(roles: List[str]):
    """
    Decorator function to check if any of the given roles are assigned to user's token.
    Returns decorated function or raises an exception if role is not assigned.

    Args:
        roles : List of roles.

    Returns:
        func : Decorated function.

    Raises:
        HTTPException : If none of the roles is assigned to user token.

    Example:

        @router.get('/getdata')
        @require_role(['admin', 'manager'])
        async def get_data():
            pass
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            for role in roles:
                if kc_realm_has_role(request, role):
                    return func(request, *args, **kwargs)
            return JSONResponse({'message': 'Acces denied'}, status_code=403)
        return wrapper
    return decorator


    """
    Decorator function to check if user's token belongs to any of the listed groups.
    Returns decorated function or raises an exception if user doesn't belong to any of the listed groups.

    Args:
        groups : List of groups.

    Returns:
        func : Decorated function.

    Raises:
        HTTPException : If user doesn't belong to any of the groups.

    Example:

        @router.get('/getdata')
        @require_group(['sample_group'])
        async def get_data():
            pass
    """
    def decorator(func):
        @wraps(func)
        def wrapper(request: Request, *args, **kwargs):
            for group in groups:
                if kc_user_in_group(request, group):
                    return func(request, *args, **kwargs)
            return JSONResponse({'message': 'Acces denied'}, status_code=403)
        return wrapper
    return decorator


def require_scope(scopes: List[str]):
    """
    This decorator function checks if the request has the required scopes. 
    If not, the function returns an HTTP 403 (Forbidden) response.
   
    Args:
        scopes (List[str]): a list of required scopes.
      
    Returns:
        The required function if the scope requirements are met, otherwise an HTTP 403 response.
        
    Example usage:
    
        @require_scope(scopes=['scope1', 'scope2'])
        async def example_endpoint(request: Request):
            ...
    """
    def decorator(func):
        @wraps(func)
        def wrapper(request: Request, *args, **kwargs):
            for scope in scopes:
                if kc_user_scope(request) == scope:
                    return func(request, *args, **kwargs)
            return JSONResponse({'message': 'Acces denied'}, status_code=403)
        return wrapper
    return decorator


def require_email_verified(func):
    """
    Decorator function to check if user's email associated with token is verified.
    Returns decorated function or raises an exception if email is not verified.

    Args:
        func : The function to be decorated.

    Returns:
        func : Decorated function.

    Raises:
        HTTPException : If email is not verified.

    Example:

        @router.get('/getdata')
        @require_email_verified
        async def get_data():
            pass
    """
    @wraps(func)
    def wrapper(request: Request, *args, **kwargs):
        if kc_user_verified_email(request):
            return func(request, *args, **kwargs)
        else:
            return JSONResponse({'message': 'Email not verified'}, status_code=403)
    return wrapper


def require_active_user(func):
    """
    Decorator function to check if the user is active.
    This function will call the original function only if the user is active, otherwise it will return a JSONResponse
    with the message "User is not active" and status code 403.

    Args:
        func : The function to be decorated.

    Returns:
        wrapper : Decorated function.

    Example:

        @router.get('/getdata')
        @require_active_user
        async def get_data():
            pass
    """
    @wraps(func)
    def wrapper(request: Request, *args, **kwargs):
        if kc_active_user(request):
            return func(request, *args, **kwargs)
        else:
            return JSONResponse({'message': 'User is not active'}, status_code=403)
    return wrapper


def require_resource_access(resource: str, role: str):
    """
    Decorator function to check if the user has access to the given resource with the given role.
    This function will call the original function only if the user has access to the resource with the given role,
    otherwise it will return a JSONResponse with a message and status code 403.

    Args:
        resource (str): The resource to be accessed.
        role (str): The role required to access the resource.

    Returns:
        wrapper : Decorated function.

    Example:

        @router.get('/getdata')
        @require_resource_access('sample_resource', 'sample_role')
        async def get_data():
            pass
    """
    def decorator(func):
        @wraps(func)
        def wrapper(request: Request, *args, **kwargs):
            resources = kc_user_resource_access(request)
            if resources and resources.get(resource, {}).get('roles', []) == role:
                return func(request, *args, **kwargs)
            else:
                return JSONResponse({'message': f'Access to resource {resource} with role {role} is required'},
                                    status_code=403)
        return wrapper
    return decorator


def require_allowed_origin(origins: list):
    """
    Decorator function to check if the request is coming from an allowed origin.
    This function will call the original function only if the request is coming from an allowed origin, otherwise it
    will return a JSONResponse with a message and status code 403.

    Args:
        origin (str): The origin to be checked.

    Returns:
        wrapper : Decorated function.

    Example:

        @router.get('/getdata')
        @require_allowed_origin('https://www.example.com')
        async def get_data():
            pass
    """
    def decorator(func):
        @wraps(func)
        def wrapper(request: Request, *args, **kwargs):
            for origin in origins:
                if origin in kc_user_allowed_origins(request):
                    return func(request, *args, **kwargs)
            else:
                return JSONResponse({'message': f'Access from origin {origin} is not allowed'}, status_code=403)
        return wrapper
    return decorator
