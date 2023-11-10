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
import json


class User:
    """
    User Class: Represents a User.

    Attributes:
        id (str): Uniquely identifies the User.
        name (str): Full name of User.
        given_name (str): User's first name.
        family_name (str): User's last name.
        preferred_username (str): The preferred username of the User.
        username (str): Username.
        email (str): User's Email Address.
        email_verified (bool): Indicates whether the email is verified.
        realm_roles (list): Roles in relation to the realm.
        resource_access (list): Information about the resources the user can access.
        active (bool): Indicates whether the User is active.
        service (str): Service provider identifier.
        scope (list): Scopes that are granted to the token.
        client_id (str): Client Identifier.
        allowed_origins (list): The origins of which are allowed.
    """
    def __init__(self, token: dict):
        """
        Constructs all the necessary attributes for the User object.

        Parameters:
            data (dict): A processed dict parsed from user info str(jwt token).
        """
        try:
            self.id = token['sub']
            self.name = token['name']
            self.given_name = token['given_name']
            self.family_name = token['family_name']
            self.preferred_username = token['preferred_username']
            self.username = token['username']
            self.email = token['email']
            self.email_verified = token['email_verified'] 
            self.realm_roles = token['realm_access']['roles'] 
            self.resource_access = [token['resource_access']] 
            self.active = token['active']
            self.service = token['azp']
            self.scope = token['scope'].split(',')
            self.client_id = token['client_id']
            self.allowed_origins = token['allowed-origins']
        except KeyError as _:
            raise Exception("Failed to init User due to missing requisite data.")

    def __repr__(self):
        """
        Represents the object as a string.
        """
        return {
            'id': self.id,
            'name': self.name,
            'given_name': self.given_name,
            'family_name': self.family_name,
            'preferred_username': self.preferred_username,
            'username': self.username,
            'email': self.email,
            'email_verified': self.email_verified,
            'realm_roles': self.realm_roles,
            'resource_access': self.resource_access,
            'active': self.active,
            'service': self.service,
            'scope': self.scope,
            'client_id': self.client_id,
            'allowed_origins': self.allowed_origins
        }


def get_user_info(token: dict):
    """
    Extracts user info from a token.

    Parameters:
        token (str): An AccessToken(jwt token) received from the server.

    Returns:
        User: User object with data extracted from the token.
    """
    return User(token)


def get_roles_resource_access(resource_access: list, resource_name: str):
    """
    Retrieves the roles of a specific resource the user can access.

    Parameters:
        resource_access (list): Information about the resources the user can access.
        resource_name (str): The name of the resource.

    Returns:
        list: A list of roles in relation to the specified resource.
    """
    for resource in resource_access:
      for rsc_name, roles in resource.items():
        if rsc_name == resource_name:
          return roles['roles']
    return None