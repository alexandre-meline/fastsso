from asgiref.sync import AsyncToSyncMiddleware
from django.http import JsonResponse
from keycloak import KeycloakOpenID
# and other necessary imports

class KeycloakSSOMiddleware(AsyncToSyncMiddleware):
    def __init__(self, get_response, *args, **kwargs):
        self.get_response = get_response
        self.server_url = kwargs.pop('server_url', '')
        self.client_id = kwargs.pop('client_id', '')
        self.realm_name = kwargs.pop('realm_name', '')
        self.client_secret_key = kwargs.pop('client_secret_key', '')

        # Get an instance of the Keycloak client
        self.keycloak_instance = KeycloakOpenID(server_url=self.server_url,
                                                client_id=self.client_id,
                                                realm_name=self.realm_name,
                                                client_secret_key=self.client_secret_key)

        super().__init__(*args, **kwargs)

    async def __call__(self, request):
        # Implement your authentication logic here similarly to your FastAPI middleware
        token = request.headers.get('Authorization', '').split(' ')[1]

        if not self.keycloak_instance.is_access_token_valid(token):
            return JsonResponse({'error': 'Invalid token'}, status=401)

        return await self.get_response(request)