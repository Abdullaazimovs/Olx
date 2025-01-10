from datetime import timedelta, datetime
from typing import List

import jwt
from fastapi import APIRouter, status, HTTPException, Depends

from config import settings
from database import crud, schemas, models
from utils import Annotations, hashing, auth_bearer
from utils.auth_bearer import JWTBearer
from utils.jwt_handler import create_access_token, create_refresh_token

router = APIRouter()


@router.post("/signup", status_code=status.HTTP_201_CREATED)
def create_user(db: Annotations.db_dependency, user_create: schemas.UserCreate):
    return crud.create_user(db, user_create)


@router.post("/login", response_model=schemas.TokenSchema)
async def login_for_access_token(form_data: Annotations.form_data, db: Annotations.db_dependency):
    user = crud.authenticate_user(form_data.email, form_data.password, db)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')

    access = create_access_token(user.email, user.id, timedelta(minutes=60))
    refresh = create_refresh_token(user.email, user.id, timedelta(days=7))

    token_db = models.TokenTable(user_id=user.id, access_toke=access, refresh_toke=refresh, status=True)

    db.add(token_db)
    db.commit()
    db.refresh(token_db)
    return {'access_token': access, 'refresh_token': refresh, 'token_type': 'bearer'}


@router.post('/logout')
def logout(db: Annotations.db_dependency, dependencies: str = Depends(JWTBearer())):
    token = dependencies
    payload = jwt.decode(token, settings.secret_key, auth_bearer.ALGORITHM)
    user_id = payload['sub']
    token_record = db.query(models.TokenTable).all()
    info = []
    for record in token_record:
        if (datetime.utcnow() - record.created_date).days > 1:
            info.append(record.user_id)
    if info:
        existing_token = db.query(models.TokenTable).where(models.TokenTable.user_id.in_(info)).delete()
        db.commit()

    existing_token = db.query(models.TokenTable).filter(models.TokenTable.user_id == user_id,
                                                        models.TokenTable.access_toke == token).first()
    if existing_token:
        existing_token.status = False
        db.add(existing_token)
        db.commit()
        db.refresh(existing_token)
    return {"message": "Logout Successfully"}


@router.post('/change-password')
def change_password(request: schemas.ChangePassword, db: Annotations.db_dependency):
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")

    if not hashing.verify_password(request.old_password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid old password")

    encrypted_password = hashing.hash_password(request.new_password)
    user.hashed_password = encrypted_password
    db.commit()

    return {"message": "Password changed successfully"}


@router.get("/users", response_model=List[schemas.UserWithPassword])
def get_users(db: Annotations.db_dependency, token: str = Depends(JWTBearer())):
    users = db.query(models.User).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found")

    # Return the users along with their passwords and other fields like id
    users_with_passwords = [{"id": user.id, "email": user.email, "password": user.hashed_password} for user in users]

    return users_with_passwords
