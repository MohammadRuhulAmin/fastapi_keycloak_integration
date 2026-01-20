from fastapi.security import OAuth2PasswordBearer
from keycloak import KeycloakOpenID
from fastapi import Security, HTTPException, status, Depends
from typing import List, Optional
from schemas import userPayload
from config.keycloak_config import settings


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=settings.token_url
)

keycloak_openid = KeycloakOpenID(
    server_url=settings.server_url,
    client_id=settings.client_id,
    realm_name=settings.realm,
    client_secret_key=settings.client_secret,
    verify=True
)


async def get_idp_public_key():
    return (
        "-----BEGIN PUBLIC KEY-----\n"
        f"{keycloak_openid.public_key()}"
        "\n-----END PUBLIC KEY-----"
    )


async def get_payload(token: str = Security(oauth2_scheme)) -> dict:
    try:
        return keycloak_openid.decode_token(
            token,
            key=await get_idp_public_key(),
            options={
                "verify_signature": True,
                "verify_aud": False,
                "verify_exp": True,
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_user_info(
    payload: dict = Depends(get_payload)
) -> userPayload:
    """
    Works for BOTH:
    - user tokens (authorization_code / password)
    - client_credentials tokens (no user info)
    """

    # detect client_credentials token
    is_client_token = "preferred_username" not in payload

    return userPayload(
        id=payload.get("sub"),
        username=payload.get("preferred_username", payload.get("clientId", "service-account")),
        email=payload.get("email", ""),
        first_name=payload.get("given_name", ""),
        last_name=payload.get("family_name", ""),
        realm_roles=payload.get("realm_access", {}).get("roles", []),
        client_roles=payload.get("resource_access", {})
            .get(settings.client_id, {})
            .get("roles", []),
    )
