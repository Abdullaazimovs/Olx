from fastapi import FastAPI

from routers import registration, announcement, category

app = FastAPI()

app.include_router(registration.router, prefix="/registration", tags=["registration"])
app.include_router(announcement.router, prefix="/announcement", tags=["announcement"])
app.include_router(category.router, prefix="/category", tags=["category"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI app!"}
