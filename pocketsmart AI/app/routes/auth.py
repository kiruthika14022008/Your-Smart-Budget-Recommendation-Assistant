from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.models.models import User

from app.schemas.schemas import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
)

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user_id,
)


router = APIRouter(
    tags=["Authentication"]
)


@router.post("/register")
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db),
):

    email = data.email.lower()

    existing_user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Email already registered",
        )

    user = User(
        name=data.name.strip(),
        email=email,
        password_hash=hash_password(
            data.password
        ),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token(
        user.id
    )

    return {
        "message": "Registration successful",
        "access_token": token,
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
        },
    }


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db),
):

    user = (
        db.query(User)
        .filter(
            User.email
            == data.email.lower()
        )
        .first()
    )

    if (
        not user
        or not verify_password(
            data.password,
            user.password_hash,
        )
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    return {
        "access_token":
            create_access_token(user.id),
        "token_type": "bearer",
    }


@router.get("/session-info")
def session_info(
    user_id: int = Depends(
        get_current_user_id
    ),
    db: Session = Depends(get_db),
):

    user = db.get(
        User,
        user_id,
    )

    return {
        "logged_in": bool(user),
        "user_id": user_id,
        "name": (
            user.name
            if user
            else None
        ),
        "email": (
            user.email
            if user
            else None
        ),
    }


@router.get("/session-data")
def session_data(
    user_id: int = Depends(
        get_current_user_id
    ),
):

    return {
        "user_id": user_id,
        "message": (
            "Session is active. "
            "Recommendation history "
            "is available at /api/history."
        ),
    }


@router.post("/logout")
def logout():

    return {
        "message": (
            "Logout successful. "
            "Remove the stored bearer token."
        )
    }


@router.post(
    "/token",
    response_model=TokenResponse,
)
def token(
    data: LoginRequest,
    db: Session = Depends(get_db),
):

    return login(
        data,
        db,
    )