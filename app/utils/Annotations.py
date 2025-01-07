from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from database.db import get_db
from fastapi.security import OAuth2PasswordRequestForm


db_dependency = Annotated[Session, Depends(get_db)]
form_data = Annotated[OAuth2PasswordRequestForm, Depends()]
