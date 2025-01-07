from fastapi import HTTPException
from sqlalchemy.orm import Session
from utils.hashing import verify_password
from database import models, schemas


def create_user(db: Session, user_create: schemas.UserCreate):
    db_user = db.query(models.User).filter(models.User.email == user_create.email).first()
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
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


def authenticate_user(email: str, password: str, db):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
