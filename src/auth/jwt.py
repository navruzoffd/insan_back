from datetime import datetime, timedelta

from fastapi.exceptions import HTTPException

from fastapi import Depends
from fastapi.security import HTTPBearer
from jose import JWTError, jwt

from ..auth.config import auth_config
from ..auth.schema import JWTData

oauth2_scheme = HTTPBearer(scheme_name="JWTBearer", bearerFormat="jwt")


def create_access_token(
    *,
    user: str,
    expires_delta: timedelta = timedelta(minutes=auth_config.JWT_EXP),
) -> str:
    jwt_data = {
        "user": user,
        "exp": datetime.utcnow() + expires_delta,
    }
    return jwt.encode(jwt_data, auth_config.JWT_SECRET, algorithm=auth_config.JWT_ALG)


async def parse_jwt_user_data_optional(
    token: str = Depends(oauth2_scheme),
) -> JWTData | None:
    if not token:
        return None

    try:
        payload = jwt.decode(
            dict(token)["credentials"],  # type: ignore
            auth_config.JWT_SECRET,
            algorithms=[auth_config.JWT_ALG],
        )
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    return JWTData(**payload)


async def parse_jwt_user_data(
    token: JWTData | None = Depends(parse_jwt_user_data_optional),
) -> JWTData:
    if not token:
        raise HTTPException(status_code=401, detail="Invalid token")

    return token
