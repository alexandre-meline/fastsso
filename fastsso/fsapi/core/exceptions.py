from fastapi.responses import JSONResponse


def unauthorized_response():
    """
    Creates a JSONResponse object indicating unauthorized response.

    Returns:
        JSONResponse object with 401 status and detail of "Non autorisé".
    """
    return JSONResponse({"detail": "Unauthorized"}, status_code=401)


def invalid_token_response():
    """
    Creates a JSONResponse object indicating response for invalid token.
    
    Returns:
        JSONResponse object with 401 status and detail of "Token invalide".
    """
    return JSONResponse({"detail": "Invalid token"}, status_code=401)


def unverified_user_response():
    """
    Return an unverified user response.
    
    Returns:
        A JSON response with a 401 status code.
    """
    return JSONResponse({"detail": "User not verified"}, status_code=401)


def keycloak_server_not_up_response():
    """
    Return a keycloak server not up response.
    
    Returns:
        A JSON response with a 500 status code.
    """
    return JSONResponse({"detail": "Failed"}, status_code=500)


def keycloak_middleware_failed_response():
    """
    Return a keycloak middleware failed response.
    
    Returns:
        A JSON response with a 500 status code.
    """
    return JSONResponse({"detail": "Failed"}, status_code=500)
