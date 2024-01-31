# Example Autodarts Refresh Token Flow

This is an example implementation of the Autodarts Refresh Token Flow.
It uses the `python-keycloak` library to handle the OAuth2 flow.
The `get_token(username: str, password: str)` function can be used to always obtain the latest token.
If the token is expired, it will automatically be refreshed.
