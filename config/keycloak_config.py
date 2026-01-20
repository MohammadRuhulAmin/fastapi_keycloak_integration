import os

from schemas import authConfiguration
from dotenv import load_dotenv

load_dotenv()

SERVER_URL = os.getenv("SERVER_URL")
REALM = os.getenv("KEYCLOAK_REALM")
CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID")
CLIENT_SECRET = os.getenv("KEYCLOAK_CLIENT_SECRET")
AUTHORIZATION_URL = os.getenv("KEYCLOAK_AUTHORIZATION_URL")
TOKEN_URL = os.getenv("KEYCLOAK_TOKEN_URL")

settings = authConfiguration(
    server_url=SERVER_URL,
    realm=REALM,
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    authorization_url=AUTHORIZATION_URL,
    token_url=TOKEN_URL,
)
print(settings)