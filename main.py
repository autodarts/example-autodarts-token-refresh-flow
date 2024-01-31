from datetime import datetime, timedelta
from time import sleep

from keycloak import KeycloakOpenID

CLIENT_ID = ""
CLIENT_SECRET = ""


class AutodartsKeycloakClient:
    token_lifetime_fraction = 0.9

    kc: KeycloakOpenID = None
    access_token: str = None
    refresh_token: str = None
    expires_at: datetime = None
    refresh_expires_at: datetime = None

    def __init__(self, *, client_id: str, client_secret: str = None):
        self.kc = KeycloakOpenID(
            server_url="https://login.autodarts.io",
            client_id=client_id,
            client_secret_key=client_secret,
            realm_name="autodarts",
            verify=True
        )

    def __set_token(self, token: dict):
        self.access_token = token['access_token']
        self.refresh_token = token['refresh_token']
        self.expires_at = datetime.now() + timedelta(
            seconds=int(self.token_lifetime_fraction * token["expires_in"])
        )
        self.refresh_expires_at = datetime.now() + timedelta(
            seconds=int(self.token_lifetime_fraction * token["refresh_expires_in"])
        )

    def __get_token(self, username: str, password: str):
        self.__set_token(self.kc.token(username, password))
        print("Getting token", self.expires_at, self.refresh_expires_at)

    def __refresh_token(self    ):
        self.__set_token(self.kc.refresh_token(self.refresh_token))
        print("Refreshing token", self.expires_at, self.refresh_expires_at)

    def get_token(self, username: str, password: str):
        if self.access_token is None:
            self.__get_token(username, password)

        now = datetime.now()
        if self.expires_at < now:
            if now < self.refresh_expires_at:
                self.__refresh_token()
            else:
                self.__get_token(username, password)

        return self.access_token

    def get_user(self):
        return self.kc.userinfo(self.access_token)


if __name__ == '__main__':
    kc = AutodartsKeycloakClient(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

    while True:
        kc.get_token('demo', 'demo')
        sleep(1)
