import json

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File,
    Form,
)

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.models.models import (
    RecommendationHistory,
)

from app.schemas.schemas import (
    HomeRequest,
    PartyRequest,
)

from app.core.security import (
    get_current_user_id,
)

from app.services.recommendation_service import (
    generate_recommendations,
)


router = APIRouter(
    tags=["Planners"]
)


# ---------------------------------------------------------
# Save history
# ---------------------------------------------------------

def save_history(
    db,
    user_id,
    planner,
    request_data,
    response_data,
):

    record = RecommendationHistory(

        user_id=user_id,

        planner=planner,

        request_json=json.dumps(
            request_data
        ),

        response_json=json.dumps(
            response_data
        ),
    )

    db.add(record)

    db.commit()

    db.refresh(record)

    return record


# =========================================================
# HOME
# =========================================================

@router.post(
    "/generate-home"
)
def generate_home(
    data: HomeRequest,

    user_id: int = Depends(
        get_current_user_id
    ),

    db: Session = Depends(get_db),
):

    request_data = data.model_dump()

    result = generate_recommendations(
        planner="home",
        data=request_data,
    )

    save_history(
        db,
        user_id,
        "home",
        request_data,
        result,
    )

    return result


# =========================================================
# PARTY
# =========================================================

@router.post(
    "/generate-party"
)
def generate_party(
    data: PartyRequest,

    user_id: int = Depends(
        get_current_user_id
    ),

    db: Session = Depends(get_db),
):

    request_data = data.model_dump()

    result = generate_recommendations(
        planner="party",
        data=request_data,
    )

    save_history(
        db,
        user_id,
        "party",
        request_data,
        result,
    )

    return result


# =========================================================
# JEWELRY
# =========================================================

@router.post(
    "/generate-jewelry"
)
async def generate_jewelry(

    budget: float = Form(...),

    occasion: str = Form(
        "Wedding"
    ),

    style: str = Form(
        "Elegant"
    ),

    outfit_color: str = Form(
        ""
    ),

    outfit_description: str = Form(
        ""
    ),

    outfit_image: UploadFile | None = File(
        None
    ),

    user_id: int = Depends(
        get_current_user_id
    ),

    db: Session = Depends(get_db),
):

    if budget <= 0:

        raise HTTPException(
            status_code=400,
            detail="Budget must be positive",
        )

    data = {

        "budget": budget,

        "occasion": occasion,

        "style": style,

        "outfit_color":
            outfit_color or None,

        "outfit_description":
            outfit_description or None,
    }

    image_bytes = None

    mime_type = None

    if outfit_image and outfit_image.filename:

        allowed_types = {
            "image/jpeg",
            "image/png",
            "image/webp",
        }

        if (
            outfit_image.content_type
            not in allowed_types
        ):

            raise HTTPException(
                status_code=400,
                detail=(
                    "Only JPG, PNG and WEBP "
                    "images are supported."
                ),
            )

        image_bytes = (
            await outfit_image.read()
        )

        max_size = (
            5 * 1024 * 1024
        )

        if len(image_bytes) > max_size:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Image must be "
                    "5MB or smaller."
                ),
            )

        mime_type = (
            outfit_image.content_type
        )

    result = generate_recommendations(
        planner="jewelry",
        data=data,
        image_bytes=image_bytes,
        mime_type=mime_type,
    )

    save_history(
        db,
        user_id,
        "jewelry",
        data,
        result,
    )

    return result


# =========================================================
# HISTORY
# =========================================================

@router.get("/history")
def history(

    user_id: int = Depends(
        get_current_user_id
    ),

    db: Session = Depends(get_db),
):

    records = (

        db.query(
            RecommendationHistory
        )

        .filter(
            RecommendationHistory.user_id
            == user_id
        )

        .order_by(
            RecommendationHistory.created_at.desc()
        )

        .limit(50)

        .all()
    )

    return [

        {

            "id": record.id,

            "planner":
                record.planner,

            "created_at":
                record.created_at.isoformat(),

            "request":
                json.loads(
                    record.request_json
                ),

            "response":
                json.loads(
                    record.response_json
                ),
        }

        for record in records
    ]


# =========================================================
# RECOMMENDATION DETAILS
# =========================================================

@router.get(
    "/recommendations-details/{history_id}"
)
def recommendation_details(

    history_id: int,

    user_id: int = Depends(
        get_current_user_id
    ),

    db: Session = Depends(get_db),
):

    record = (

        db.query(
            RecommendationHistory
        )

        .filter(

            RecommendationHistory.id
            == history_id,

            RecommendationHistory.user_id
            == user_id,

        )

        .first()
    )

    if not record:

        raise HTTPException(
            status_code=404,
            detail="Recommendation not found",
        )

    return json.loads(
        record.response_json
    )