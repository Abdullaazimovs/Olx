from fastapi import APIRouter, status, Depends

from database import crud, schemas
from utils import Annotations
from utils.auth_bearer import JWTBearer

router = APIRouter()


@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=schemas.AnnouncementSchema)
def create_announcement(
        db: Annotations.db_dependency,
        announcement_create: schemas.AnnouncementSchema,
        token: str = Depends(JWTBearer())
):
    return crud.create_announcement(db, announcement_create)
