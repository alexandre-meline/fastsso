# User Information Module (`core/currentuser.py`)

The `core/currentuser.py` module in the `fsapi` package provides a suite of functions designed to extract and interact with authenticated user information retrieved from Keycloak tokens. These utilities power the security features of the FastAPI application by securing endpoints and ensuring user data is appropriately handled and accessible.

## Overview

Once a user is authenticated through the Keycloak SSO, their token can be processed to extract various pieces of information such as roles, group memberships, email verification status, active status, and more. The `core/currentuser.py` module makes this process seamless, and the information readily available for use within FastAPI routes.

## Functions

Below is a summary of the main functions provided by the module and their usage:

### `kc_user`

- **Description**: Retrieves the authenticated user's object from the request.
- **Parameters**: `request: Request`
- **Returns**: `User` object if authenticated, otherwise `None`.
- **Usage Example**: `user_data = kc_user(request)`

### `kc_get_user_info`

- **Description**: Fetches specific user information by attribute name from the authenticated request.
- **Parameters**: `request: Request, attr: str`
- **Returns**: The corresponding attribute value, or `None` if not authenticated.
- **Usage Example**: `user_email = kc_get_user_info(request, "email")`

### `kc_user_id`, `kc_user_email`, `kc_user_first_name`, etc.

- **Descriptions**: Return specific user information such as user ID, email, first name, etc.
- **Parameters**: `request: Request`
- **Returns**: Corresponding data if authenticated, otherwise `None`.
- **Usage Examples**: 
  - `user_id = kc_user_id(request)`
  - `user_email = kc_user_email(request)`

### `kc_realm_has_role`

- **Description**: Checks if the authenticated user has the specified role in the realm.
- **Parameters**: `request: Request, role: str`
- **Returns**: `True` if the user has the role, `False` otherwise.
- **Usage Example**: `if kc_realm_has_role(request, "admin"): ...`

### `kc_user_scope`

- **Description**: Retrieves the authenticated user's scope from the request state.
- **Parameters**: `request: Request`
- **Returns**: User's scope if authenticated, otherwise `None`.
- **Usage Example**: `user_scope = kc_user_scope(request)`

### `kc_active_user`

- **Description**: Determines if the authenticated user is active.
- **Parameters**: `request: Request`
- **Returns**: `True` if active, otherwise `None`.
- **Usage Example**: `if kc_active_user(request): ...`

### `kc_user_resource_access`

- **Description**: Extracts the resource access details of the authenticated user.
- **Parameters**: `request: Request`
- **Returns**: Resource access details if authenticated, otherwise `None`.
- **Usage Example**: 
  - `resource_access = kc_user_resource_access(request)`

## Conclusion

`fsapi` leverages the powerful capabilities of Keycloak for user authentication and provides the `core/currentuser.py` module as an essential part of its security functionality. By utilizing the functions in this module, developers can easily enforce authorization rules and ensure that user identities and permissions are correctly recognized and managed throughout their FastAPI applications.