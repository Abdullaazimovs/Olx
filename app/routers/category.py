from typing import List
from utils.auth_bearer import JWTBearer

from fastapi import APIRouter, status, Depends

from database import crud, schemas, models
from utils import Annotations

router = APIRouter()


@router.post("/create_category", status_code=status.HTTP_201_CREATED, response_model=schemas.CategoryCreate)
def create_category(
        db: Annotations.db_dependency,
        category_create: schemas.CategoryCreate,
        token: str = Depends(JWTBearer())
):
    return crud.create_category(db, category_create)


@router.get("/category_all", status_code=status.HTTP_200_OK, response_model=List[schemas.CategorySchemaWithCount])
def list_categories(db: Annotations.db_dependency, token: str = Depends(JWTBearer())):
    categories = db.query(models.Category).all()
    for category in categories:
        category.announcements_count = len(category.announcements)
    return categories
