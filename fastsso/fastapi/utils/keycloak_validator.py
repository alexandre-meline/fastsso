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
from keycloak import KeycloakOpenID
from keycloak.exceptions import KeycloakAuthenticationError
from fastsso.fastapi.utils.user import User, get_user_info, get_roles_resource_access


class keycloakValidator:

    def __init__(self,  server_url: str,
                        client_id: str,
                        realm_name: str,
                        client_secret_key: str,
                        custom_headers: dict = None,
                        proxies: dict = None,
                        timeout: int = None):
        
        self.server_url = server_url
        self.client_id = client_id
        self.realm_name = realm_name
        self.client_secret_key = client_secret_key
        self.custom_headers = custom_headers
        self.proxies = proxies
        self.timeout = timeout

        self.keycloak_openid = self.keycloak_validate_connection()

    def keycloak_validate_connection(self) -> bool:
        """
        Validate the connection to the Keycloak server.

        Returns:
            KeycloakOpenID: The KeycloakOpenID object.
        """
        # Etablish connection to Keycloak server
        keycloak_openid = KeycloakOpenID(server_url=self.server_url,
                                        client_id=self.client_id,
                                        realm_name=self.realm_name,
                                        client_secret_key=self.client_secret_key,
                                        custom_headers=self.custom_headers,
                                        verify=True,
                                        proxies=self.proxies,
                                        timeout=self.timeout)
        try:
            # Get well-known from Keycloak server
            if keycloak_openid.well_known():
                # Set KeycloakOpenID object
                self.keycloak_openid = keycloak_openid
                # Return True if connection is successful
                return True
            # Return False if connection is unsuccessful
            return False
        # Return False if connection is unsuccessful
        except KeycloakAuthenticationError as e:
            return False


    def token_to_user_info(self, token: str) -> User:
        """
        Validate a token string and return the token's info as a DICT object.

        Args:
            token (`str`): The token to be validated.
        
        Returns:
            dict: The token's info as a DICT object.
        """
        try:
            # Get token info from Keycloak server
            introspect_resp = self.keycloak_openid.introspect(token)
            # Check if token user is active
            if self.__active_user(introspect_resp):
                # Return token info to dict
                return introspect_resp
            # Return None if token user is not active
            return None
        # Return None if token is invalid
        except KeycloakAuthenticationError as e:
            return None
    

    def __active_user(self, introspect_resp: dict) -> bool:
        """
        Validate if the user is active.
        
        Args:
            introspect_resp (`dict`): The token's introspect response.
            
        Returns:    
            bool: True if user is active, False otherwise.
        """
        # Return True if user is active, False otherwise
        return True if introspect_resp['active'] else False
        