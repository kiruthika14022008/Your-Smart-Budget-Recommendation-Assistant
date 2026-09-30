from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

from fastapi import (
    Depends,
    HTTPException,
    status,
)

from fastapi.security import OAuth2PasswordBearer

from werkzeug.security import (
    generate_password_hash,
    check_password_hash,
)

from app.core.config import settings


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/token",
    auto_error=False,
)


ALGORITHM = "HS256"


def hash_password(password: str) -> str:

    return generate_password_hash(password)


def verify_password(
    password: str,
    hashed_password: str,
) -> bool:

    return check_password_hash(
        hashed_password,
        password,
    )


def create_access_token(user_id: int):

    expiration = (
        datetime.now(timezone.utc)
        + timedelta(hours=24)
    )

    payload = {
        "sub": str(user_id),
        "exp": expiration,
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=ALGORITHM,
    )


def get_current_user_id(
    token: str = Depends(oauth2_scheme),
):

    if not token:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Login required",
        )

    try:

        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise ValueError()

        return int(user_id)

    except (
        JWTError,
        ValueError,
        TypeError,
    ):

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )