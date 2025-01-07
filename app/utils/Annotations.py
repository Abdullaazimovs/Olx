from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from database.db import get_db
from fastapi import Form


class EmailPasswordForm:
    def __init__(self, email: str = Form(...), password: str = Form(...)):
        self.email = email
        self.password = password


db_dependency = Annotated[Session, Depends(get_db)]
form_data = Annotated[EmailPasswordForm, Depends()]
