from fastapi import FastAPI

from routers import registration

app = FastAPI()

app.include_router(registration.router, prefix="/registration", tags=["registration"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI app!"}
