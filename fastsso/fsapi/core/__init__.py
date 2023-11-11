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

from fastsso.fsapi.core.exceptions import (unauthorized_response,
                                            invalid_token_response,
                                            unverified_user_response,
                                            keycloak_server_not_up_response,
                                            keycloak_middleware_failed_response)

from fastsso.fsapi.core.logging import logger