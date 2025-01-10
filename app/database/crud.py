from fastapi import HTTPException, status

from pathlib import Path
from database import models, schemas
from utils.Annotations import db_dependency
from utils.hashing import verify_password


def create_user(db: db_dependency, user_create: schemas.UserCreate):
    db_user = db.query(models.User).filter(models.User.email == user_create.email).first()
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    db_user = db.query(models.User).filter(models.User.username == user_create.username).first()
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Username already taken"
        )

    db_user = models.User(
        username=user_create.username,
        email=user_create.email,
        hashed_password=user_create.password,
        first_name=user_create.first_name,
        last_name=user_create.last_name,
        phone_number=user_create.phone_number,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


async def create_announcement(db: db_dependency, create_announcement: schemas.AnnouncementSchema):
    photo_url = None

    if create_announcement.photo:
        file_path = Path("app/media/images")
        file_location = file_path / create_announcement.photo.filename
        try:
            with open(file_location, "wb", errors='ignore') as file:
                file.write(await create_announcement.photo.read())
            photo_url = f"http://localhost:8080/media/images/{create_announcement.photo.filename}"
        except Exception as e:
            raise HTTPException(status_code=500, detail="Error uploading file.")

    elif create_announcement.photo_url:
        photo_url = create_announcement.photo_url

    category = db.query(models.Category).filter(models.Category.id == create_announcement.category_id)

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    # Create the announcement
    db_announcement = models.Announcement(
        title=create_announcement.title,
        category_id=create_announcement.category_id,
        photo=photo_url,
        description=create_announcement.description,
        location=create_announcement.location
    )

    db.add(db_announcement)
    db.commit()
    db.refresh(db_announcement)
    return db_announcement


def create_category(db: db_dependency, category_create: schemas.CategoryCreate):
    existing_category = db.query(models.Category).filter(models.Category.name == category_create.name).first()
    if existing_category:
        raise HTTPException(status_code=400, detail="Category already exists")

    new_category = models.Category(name=category_create.name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


def authenticate_user(email: str, password: str, db):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email")
    if not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password"
        )
    return user
